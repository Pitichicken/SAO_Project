{
  description = "Sao Project - BCI EEG - motor imagery classification";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      python = pkgs.python3.withPackages (ps: with ps; [
        numpy
        scipy
        pandas
        matplotlib
        scikit-learn
        mne
        ipykernel
        jupyter
        tkinter
      ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ python ];
        shellHook = ''
          export MNE_DATA="$PWD/data"
          echo ""	
   	  echo "Link Start -- Loaded Libraries: MNE, Scikit-Learn, Pandas, Jupyter"
	  echo ""
          echo "env ready with python version: $(python --version)"
        '';
      };
    };
}
