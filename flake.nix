{
  description = "Expose CUDA devices inside Nix builds";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }: {
    nixosModules = rec {
      expose-cuda = import ./default.nix;
      default = expose-cuda;
    };
  };
}
