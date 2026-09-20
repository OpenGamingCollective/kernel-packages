{
  description = "OpenGamingCollective Kernel Packages";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    {
      packages.x86_64-linux =
        let
          pkgs = nixpkgs.legacyPackages.x86_64-linux;
          lib = pkgs.lib;
        in
        {
          default = lib.recurseIntoAttrs (pkgs.linuxPackagesFor self.packages."x86_64-linux".linux-ogc);
          linux-ogc = pkgs.callPackage ./nix/package.nix { };
        };
    };
}
