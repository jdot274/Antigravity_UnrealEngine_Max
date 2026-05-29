{ pkgs }: {
  deps = [
    pkgs.gcc
    pkgs.gnumake
    pkgs.clang-tools   # clangd LSP for code completion
  ];
}
