{ pkgs, ... }: {
  nix.settings.system-features = [ "expose-cuda" ];
  nix.settings.pre-build-hook = pkgs.writers.writePython3 "nix-pre-build.py" { }
    (builtins.readFile ./nix-pre-build-hook.py);
}
