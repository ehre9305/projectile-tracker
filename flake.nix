{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  outputs = { self, nixpkgs }: {
    devShell.x86_64-linux = with nixpkgs.legacyPackages.x86_64-linux; mkShell {
      buildInputs = with python3Packages; [
        python3
        zlib
        numpy
        pandas
		pyqtgraph
	    (opencv4.override { enableGtk2 = true; })
		pyqt6
        # Add other Python packages that your project depends on
      ];
    };
  };
}

