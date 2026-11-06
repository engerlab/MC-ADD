# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                                   :::
# :::                 R U N    F I L E                  :::
# :::                                                   :::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# This file runs the simulation in interactive mode (ONLY for visualization)
# and in bash mode (NO visualzation)


if [ "$1" == "--vis" ]; then                           # Verifies if the visualization argument (--vis) has been given
    $G4WORKDIR/bin/$G4SYSTEM/MC-ADD --vis
else
    $G4WORKDIR/bin/$G4SYSTEM/MC-ADD MC-ADD.mac 123456
fi