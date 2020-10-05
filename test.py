import operator
import json
import sys
import os.path
import requests

SUGGESTIONS = []
ALLOWED_VERSIONS = ['eleven', 'ten', 'ten_plus', 'pie', 'pie_plus']
WIKI_BASE_URL = 'https://raw.githubusercontent.com/PixelExperience/wiki/master/_data/devices'


def test_integrity_devices():
    try:
        devices = json.loads(open('devices.json', 'r').read())
    except:
        SUGGESTIONS.append('devices.json is not a valid JSON.')
        return

    for device in devices:
        device_index = devices.index(device)
        if 'name' not in device:
            SUGGESTIONS.append(
                f"'name' key not found in devices.json for device index value {device_index}")

        if 'brand' not in device:
            SUGGESTIONS.append(
                f"'brand' key not found in devices.json for device index value {device_index}")

        if 'codename' not in device:
            SUGGESTIONS.append(
                f"'codename' key not found in devices.json for device index value {device_index}")
        else:
            codename = device.get('codename')
            if not os.path.isfile(f"images/{codename}.png"):
                SUGGESTIONS.append(
                    f"images/{codename}.png not found for codename {codename} in devices.json for device index value {device_index}")
            yaml = requests.head(f"{WIKI_BASE_URL}/{codename}.yml")
            if yaml.status_code != 200:
                SUGGESTIONS.append(
                    f"Wiki YAML not found for codename {codename} in devices.json for device index value {device_index}")

        if 'supported_versions' not in device:
            SUGGESTIONS.append(
                f"'supported_versions' key not found in devices.json for index value {device_index}")
            continue

        supported_versions = device['supported_versions']
        for supported_version in supported_versions:
            version_index = supported_versions.index(supported_version)
            if 'version_code' not in supported_version:
                SUGGESTIONS.append(
                    f"'version_code' key not found in devices.json for device index value {device_index} and version index value {version_index}")

            if supported_version['version_code'] not in ALLOWED_VERSIONS:
                SUGGESTIONS.append(
                    f"'version_code' key has a value that is not allowed in devices.json for device index value {device_index} and version index value {version_index}")
    return


def test_integrity_team():
    try:
        lead = json.loads(open('team/lead.json', 'r').read())
    except:
        SUGGESTIONS.append('team/lead.json is not a valid JSON.')
        return

    try:
        core = json.loads(open('team/core.json', 'r').read())
    except:
        SUGGESTIONS.append('team/core.json is not a valid JSON.')
        return

    try:
        maintainers = json.loads(open('team/maintainers.json', 'r').read())
    except:
        SUGGESTIONS.append('team/maintainers.json is not a valid JSON.')
        return

    for member in maintainers:
        member_index = maintainers.index(member)
        if 'name' not in member:
            SUGGESTIONS.append(
                f"'name' key not found in maintainers.json for member index value {member_index}")

        if 'country' not in member:
            SUGGESTIONS.append(
                f"'country' key not found in maintainers.json for member index value {member_index}")

        if 'github_username' not in member:
            SUGGESTIONS.append(
                f"'github_username' key not found in maintainers.json for member index value {member_index}")

        if 'devices' not in member:
            SUGGESTIONS.append(
                f"'devices' key not found in maintainers.json for member index value {member_index}")
            continue

        devices = member['devices']
        for device in devices:
            device_index = devices.index(device)
            if 'codename' not in device:
                SUGGESTIONS.append(
                    f"'codename' key not found in maintainers.json for member index value {member_index} and device index value {device_index}")

            if 'versions' not in device:
                SUGGESTIONS.append(
                    f"'versions' key not found in maintainers.json for member index value {member_index}")
                continue

            versions = device['versions']
            for version in versions:
                version_index = versions.index(version)

                if version not in ALLOWED_VERSIONS:
                    SUGGESTIONS.append(
                        f"'versions' key has a value that is not allowed in maintainers.json for device index value {device_index} and version index value {version_index} and member index value {member_index}")

    devices = lead['devices']
    for device in devices:
        device_index = devices.index(device)
        if 'codename' not in device:
            SUGGESTIONS.append(
                f"'codename' key not found in lead.json  for device index value {device_index}")

            if 'versions' not in device:
                SUGGESTIONS.append(
                    f"'versions' key not found in lead.json for device index value {device_index}")
                continue

            versions = device['versions']
            for version in versions:
                version_index = versions.index(version)

                if version not in ALLOWED_VERSIONS:
                    SUGGESTIONS.append(
                        f"'versions' key has a value that is not allowed in lead.json for device index value {device_index} and version index value {version_index}")

    if 'name' not in lead:
        SUGGESTIONS.append(
            f"'name' key not found in lead.json")

    if 'country' not in lead:
        SUGGESTIONS.append(
            f"'country' key not found in lead.json")

    if 'github_username' not in lead:
        SUGGESTIONS.append(
            f"'github_username' key not found in lead.json")

    if 'devices' not in lead:
        SUGGESTIONS.append(
            f"'devices' key not found in lead.json")

    for member in core:
        member_index = core.index(member)
        if 'name' not in member:
            SUGGESTIONS.append(
                f"'name' key not found in core.json for member index value {member_index}")

        if 'country' not in member:
            SUGGESTIONS.append(
                f"'country' key not found in core.json for member index value {member_index}")

        if 'github_username' not in member:
            SUGGESTIONS.append(
                f"'github_username' key not found in core.json for member index value {member_index}")

        if 'devices' not in member:
            SUGGESTIONS.append(
                f"'devices' key not found in core.json for member index value {member_index}")
            continue

        devices = member['devices']
        for device in devices:
            device_index = devices.index(device)
            if 'codename' not in device:
                SUGGESTIONS.append(
                    f"'codename' key not found in core.json for member index value {member_index} and device index value {device_index}")

            if 'versions' not in device:
                SUGGESTIONS.append(
                    f"'versions' key not found in core.json for member index value {member_index}")
                continue

            versions = device['versions']
            for version in versions:
                version_index = versions.index(version)

                if version not in ALLOWED_VERSIONS:
                    SUGGESTIONS.append(
                        f"'versions' key has a value that is not allowed in core.json for device index value {device_index} and version index value {version_index} and member index value {member_index}")

    return


def format_json():
    # Load JSON's
    devices = json.loads(open('devices.json', 'r').read())
    lead = json.loads(open('team/lead.json', 'r').read())
    core = json.loads(open('team/core.json', 'r').read())
    maintainers = json.loads(open('team/maintainers.json', 'r').read())

    # Sort JSON alphabatically with selected keys
    devices = sorted(devices, key=operator.itemgetter('codename', 'brand'))
    #lead = sorted(lead, key=operator.itemgetter('name', 'country'))
    core = sorted(core, key=operator.itemgetter('name', 'country'))
    maintainers = sorted(
        maintainers, key=operator.itemgetter('name', 'country'))

    # Dump them
    devices = json.dumps(devices, indent=3, sort_keys=False)
    lead = json.dumps(lead, indent=3, sort_keys=False)
    core = json.dumps(core, indent=3, sort_keys=False)
    maintainers = json.dumps(maintainers, indent=3, sort_keys=False)

    # Open JSON's
    devices_json = open('devices.json', 'w')
    lead_json = open('team/lead.json', 'w')
    core_json = open('team/core.json', 'w')
    maintainers_json = open('team/maintainers.json', 'w')

    # Write dump's
    devices_json.write(devices)
    lead_json.write(lead)
    core_json.write(core)
    maintainers_json.write(maintainers)

    # Close JSON's
    devices_json.close()
    lead_json.close()
    core_json.close()
    maintainers_json.close()

    return 0


def main():
    print('Running Integrity tests for all the JSON\'s.')
    test_devices = test_integrity_devices()
    test_team = test_integrity_team()

    if len(SUGGESTIONS) > 0:
        print('Integrity test for one or more JSON\'s failed. Cannot proceed with JSON formatter.\n\n')
        print('Below might be the reasons for test failure.')
        for SUGGESTION in SUGGESTIONS:
            print(SUGGESTION)
        sys.exit(1)
    else:
        print('Integrity test passed successfully. Now formatting all the JSON\'s')
        format_json()
        sys.exit(0)


if __name__ == "__main__":
    main()
