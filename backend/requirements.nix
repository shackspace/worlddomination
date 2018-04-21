# generated using pypi2nix tool (version: 1.8.0)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -V3.6 -r ./reqs
#

{ pkgs ? import <nixpkgs> {}
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python36;
  };

  commonBuildInputs = [];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreter = pythonPackages.buildPythonPackage {
        name = "python36-interpreter";
        buildInputs = [ makeWrapper ] ++ (builtins.attrValues pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter}               $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "               (builtins.attrValues pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -f $prog ]; then
                  ln -s $prog $out/bin/`basename $prog`
                fi
              done
            fi
          done
          for prog in "$out/bin/"*; do
            wrapProgram "$prog" --prefix PYTHONPATH : "$PYTHONPATH"
          done
          pushd $out/bin
          ln -s ${pythonPackages.python.executable} python
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };
    in {
      __old = pythonPackages;
      inherit interpreter;
      mkDerivation = pythonPackages.buildPythonPackage;
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (drv.drvAttrs // f drv.drvAttrs);
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {

    "LinkHeader" = python.mkDerivation {
      name = "LinkHeader-0.4.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/27/d4/eb1da743b2dc825e936ef1d9e04356b5701e3a9ea022c7aaffdf4f6b0594/LinkHeader-0.4.3.tar.gz"; sha256 = "7fbbc35c0ba3fbbc530571db7e1c886e7db3d718b29b345848ac9686f21b50c3"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ pythonPackages.requests ];
      meta = with pkgs.stdenv.lib; {
        homepage = "";
        license = licenses.bsdOriginal;
        description = "Parse and format link headers according to RFC 5988 \"Web Linking\"";
      };
    };



    "aiocoap" = python.mkDerivation {
      name = "aiocoap-0.3";
      src = pkgs.fetchurl { url = "https://pypi.python.org/packages/9c/f6/d839e4b14258d76e74a39810829c13f8dd31de2bfe0915579b2a609d1bbe/aiocoap-0.3.tar.gz"; sha256 = "402d4151db6d8d0b1d66af5b6e10e0de1521decbf12140637e5b8d2aa9c5aef6"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."LinkHeader"
      pythonPackages.docopt
      (pythonPackages.buildPythonPackage rec {
    pname = "grequests";
    version = "0.3.1";
    name = "${pname}-${version}";

    src = pkgs.fetchFromGitHub {
      owner = "kennethreitz";
      repo = "grequests";
      rev =  "d1e70eb";
      sha256 = "0drfx4fx65k0g5sj0pw8z3q1s0sp7idn2yz8xfb45nd6v82i37hc";
    };

    doCheck = false;

    propagatedBuildInputs = with pythonPackages; [ requests gevent ];

  })

    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "";
        license = licenses.mit;
        description = "Python CoAP library";
      };
    };

  };
  overrides = import ./requirements_override.nix { inherit pkgs python; };
  commonOverrides = [

  ];

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            ([overrides] ++ commonOverrides)
         )
   )
