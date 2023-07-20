# nixos-expose-cuda

Expose CUDA devices inside Nix builds.

See discussion in https://github.com/NixOS/nixpkgs/issues/225912.

Nix's sandboxed builds forbids access to some files necessary for CUDA applications, like `/dev/nvidia*` and `libcuda.so` (in `/run/opengl-driver/lib` in NixOS). This NixOS module allows any derivation to request access to them by setting the `requiredSystemFeatures = [ "expose-cuda" ]` attribute.

Hopefully this will not be necessary in the future.

Code taken from this gist: https://gist.github.com/SomeoneSerge/4832997ab09e4e71301e5469eec3066a.


# Usage

Just import `default.nix` as a NixOS module. If you use flakes:

```nix
{
...
  inputs.expose-cuda.url = "github:ogoid/nixos-expose-cuda";
  inputs.expose-cuda.inputs.nixpkgs.follows = "nixpkgs";
...
  outputs = { nixpkgs, expose-cuda, ...}: {
    nixosConfigurations = {
      ... nixpkgs.lib.nixosSystem {
        modules = [ expose-cuda.nixosModules.default ];
      ...
  }
}
```

With this configuration any derivation with the `requiredSystemFeatures = [ "expose-cuda" ]` attribute should be able to access CUDA during build.