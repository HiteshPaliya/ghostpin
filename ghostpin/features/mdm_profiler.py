"""
GhostPin v5.0 — Feature: MDM & EMM Profiler
Detects Mobile Device Management enrollment, policies, and vendor-specific DPC apps.
"""

import re
from ghostpin.core.adb import adb_shell, run_cmd

# Known MDM/EMM vendor package names
MDM_VENDORS = {
    'com.mobileiron': 'MobileIron / Ivanti',
    'com.mobileiron.anyware.android': 'MobileIron Core',
    'com.microsoft.intune': 'Microsoft Intune',
    'com.microsoft.windowsintune.companyportal': 'Intune Company Portal',
    'com.jamf.management.jamfnow': 'Jamf Now',
    'com.jamfsoftware.jamfnow': 'Jamf Pro',
    'com.vmware.horizon': 'VMware Workspace ONE Horizon',
    'com.airwatch.androidagent': 'VMware Workspace ONE (AirWatch)',
    'com.soti.mobicontrol': 'SOTI MobiControl',
    'com.citrix.mdx.mdxManager': 'Citrix XenMobile',
    'com.maas360.android.core': 'IBM MaaS360',
    'com.hexnode.mdm': 'Hexnode MDM',
    'com.blackberry.work': 'BlackBerry UEM',
    'com.samsung.android.knox.analytics.uploader': 'Samsung Knox',
    'com.android.managedprovisioning': 'Android Enterprise (Work Profile)',
    'com.google.android.apps.work.clouddpc': 'Android Enterprise Cloud DPC',
}

DEVICE_ADMIN_MARKER = 'Device Administrators:'
WORK_PROFILE_MARKER = 'work'

MDM_BYPASS_JS = r"""
// GhostPin MDM Profiler — Policy Hooks
// Hooks DevicePolicyManager to log active restrictions

Java.perform(function() {
  var TAG = '[GPMonitor:MDM]';
  var log = function(m) { send(TAG + ' ' + m); };

  try {
    var DPM = Java.use('android.app.admin.DevicePolicyManager');

    // Log active device admin check
    DPM.isAdminActive.implementation = function(comp) {
      var result = this.isAdminActive(comp);
      log('isAdminActive: ' + comp + ' => ' + result);
      return result;
    };

    // Log device owner
    DPM.isDeviceOwnerApp.implementation = function(pkg) {
      var result = this.isDeviceOwnerApp(pkg);
      log('isDeviceOwnerApp: ' + pkg + ' => ' + result);
      return result;
    };

    // Log profile owner
    DPM.isProfileOwnerApp.implementation = function(pkg) {
      var result = this.isProfileOwnerApp(pkg);
      log('isProfileOwnerApp: ' + pkg + ' => ' + result);
      return result;
    };

    // Policy restriction reads
    ['getUserRestrictions', 'getPasswordQuality', 'getKeyguardDisabledFeatures',
     'getMaximumFailedPasswordsForWipe', 'getPasswordExpirationTimeout'].forEach(function(method) {
      try {
        DPM[method].overloads.forEach(function(ol) {
          ol.implementation = function() {
            var result = ol.call(this, Array.from(arguments));
            log(method + ' => ' + result);
            return result;
          };
        });
      } catch(e) {}
    });

    log('MDM policy hooks active');
  } catch(e) {
    log('DevicePolicyManager not found: ' + e);
  }
});
"""

def profile_device(serial: str) -> dict:
    """Perform full MDM profiling of a device."""
    result = {
        'serial': serial,
        'mdm_detected': False,
        'vendors': [],
        'device_admins': [],
        'work_profile': False,
        'knox_enabled': False,
        'policies': {},
        'installed_mdm_apps': [],
        'risk_level': 'none',
        'bypass_script': MDM_BYPASS_JS,
        'notes': [],
    }

    # 1. Check installed packages for MDM vendors
    installed = adb_shell(serial, 'pm list packages')
    for pkg, vendor in MDM_VENDORS.items():
        if pkg in installed:
            result['installed_mdm_apps'].append({'package': pkg, 'vendor': vendor})
            result['vendors'].append(vendor)
            result['mdm_detected'] = True

    # 2. Check device admins
    admin_out = adb_shell(serial, 'dpm list-owners 2>/dev/null || dumpsys device_policy 2>/dev/null | grep -A3 "Device Administrators"')
    if admin_out:
        result['device_admins'] = [l.strip() for l in admin_out.split('\n') if l.strip() and 'mAdminList' not in l]
        if result['device_admins']:
            result['mdm_detected'] = True

    # 3. Check for Work Profile
    users_out = adb_shell(serial, 'pm list users')
    if 'work' in users_out.lower() or 'UserInfo{10' in users_out:
        result['work_profile'] = True
        result['mdm_detected'] = True
        result['notes'].append('Work Profile (Android Enterprise) detected — personal/work isolation active')

    # 4. Check Knox (Samsung)
    knox_out = adb_shell(serial, 'getprop ro.knox.version 2>/dev/null')
    if knox_out and knox_out != '':
        result['knox_enabled'] = True
        result['notes'].append(f'Samsung Knox version: {knox_out}')

    # 5. Check policy enforcement
    policy_checks = {
        'screen_lock_policy': 'settings get global lock_screen_owner_info_enabled',
        'usb_debugging_policy': 'settings get global adb_enabled',
        'screen_capture_disabled': 'settings get secure bluetooth_on',
        'vpn_always_on': 'dumpsys connectivity | grep -i vpn | head -3',
    }
    for policy_name, cmd in policy_checks.items():
        val = adb_shell(serial, cmd)
        if val:
            result['policies'][policy_name] = val.strip()

    # 6. Determine risk level
    if result['vendors']:
        vendor_names = ', '.join(result['vendors'])
        result['risk_level'] = 'high'
        result['notes'].insert(0, f'MDM software detected: {vendor_names}')
        result['notes'].append('MDM policy hooks recommended — inject mdm_bypass script via GhostPin')
    elif result['device_admins']:
        result['risk_level'] = 'medium'
        result['notes'].append('Device admin apps active — MDM restrictions may apply')

    return result
