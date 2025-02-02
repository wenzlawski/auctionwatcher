{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = inputs @ {self, ...}:
    inputs.flake-utils.lib.eachDefaultSystem (system: let
      pkgs = inputs.nixpkgs.legacyPackages.${system};

      pyPkgs = with pkgs.python3Packages; [
        scrapy
        jinja2
        humanize
        dateparser
        platformdirs
      ];

      python' = pkgs.python3.withPackages (ps: pyPkgs);

      nativeBuildInputs = with pkgs; [
        python'
      ];
    in {
      devShells.default = pkgs.mkShell {inherit nativeBuildInputs;};

      packages.default = pkgs.python3.pkgs.buildPythonApplication {
        name = "auctionwatcher";
        version = "0.0.1";
        src = ./.;
        format = "pyproject";

        propagatedBuildInputs = pyPkgs;

        nativeBuildInputs =
          nativeBuildInputs
          ++ [
          ];

        pythonImportsCheck = [
          "auctionwatcher"
        ];
      };
    });
}
