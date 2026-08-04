{
  lib,
  fetchurl,
  buildLinux,
  ...
}:
let
  kernel-version = "6.19.14";
  ogc-revision = "ogc2";
  version = "${kernel-version}-${ogc-revision}";
  kernelSrc = fetchurl {
    url = "https://github.com/OpenGamingCollective/linux/archive/refs/tags/v${version}.tar.gz";
    hash = "sha256-LfrHohmdIW/YCU4LYrWYLcqItTSSHUQ9iLnfnR0o9Gc=";
  };
  configs = [
    ../config/ogc.config.set
    ../config/ogc.config.unset
  ];

  # Build the structured kernel config from one or more configs from the `configs` array
  kernelConfig = lib.pipe configs [
    # Read each config file into a string
    (configs: map (config: builtins.readFile config) configs)
    # Join all configs into a single string
    (configs: lib.strings.join "\n" configs)
    # Split the single config into lines
    (config: lib.strings.splitString "\n" config)
    # Find all lines that start with "CONFIG_"
    (lines: lib.strings.filter (line: (builtins.match "^CONFIG_.*" line) != null) lines)
    # Strip the "CONFIG_" prefix of each kernel option so it can be in `structuredExtraConfig` format
    # E.g. "CONFIG_NTSYNC=m" -> "NTSYNC=m"
    (lines: map (line: lib.strings.removePrefix "CONFIG_" line) lines)
    # Convert each stripped line into key/value pairs
    # E.g. "NTSYNC=m" -> ["NTSYNC" "m"]
    (lines_stripped: map (line: builtins.split "=" line) lines_stripped)
    # Convert each key/value pair into an attribute set in the form of: {"name" = key; "value" = value;}
    # E.g. ["NTSYNC" "m"] -> {"name" = "NTSYNC"; "value" = lib.kernel.module;}
    (kvPairs: map kvpairToOption kvPairs)
    # Convert the list of attribute sets into a single combined attribute set that will
    # be used as the `structuredExtraConfig`.
    # E.g.
    # {
    #   NTSYNC = lib.kernel.module;
    #   HID_ASUS = lib.kernel.module;
    #   ...
    # }
    (attrSets: builtins.listToAttrs attrSets)
  ];

  # Function for converting a key/value pair into a kernel option attribute set
  # E.g. "NTSYNC=m" -> {"name": "NTSYNC", "value": lib.kernel.module}
  kvpairToOption =
    kv_pair:
    if (builtins.length kv_pair) == 1 then
      let
        key = builtins.elemAt kv_pair 0;
      in
      {
        "name" = key;
        "value" = lib.mkDefault lib.kernel.unset;
      }
    else
      let
        key = builtins.elemAt kv_pair 0;
        value = builtins.elemAt kv_pair 1;
      in
      {
        "name" = key;
        "value" =
          if value == "y" then
            lib.mkDefault lib.kernel.yes
          else if value == "m" then
            lib.mkDefault lib.kernel.module
          else if value == "n" then
            lib.mkDefault lib.kernel.no
          else
            lib.mkDefault lib.kernel.unset;
      };
in

buildLinux {
  version = version;
  modDirVersion = version;
  src = kernelSrc;

  structuredExtraConfig = {
    LOCALVERSION = lib.kernel.freeform "-${ogc-revision}";
  }
  // kernelConfig;
}
