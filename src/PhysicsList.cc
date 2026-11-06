// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::        Source file for Physics List           :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries 
#include "PhysicsList.hh"


// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

PhysicsList::PhysicsList()
{
    // ::: Physics Libraries :::
    // The EM physics constructor defined below is the one used in the simulation (see ConstructProcess()).
    // Select it according to the application:
    // G4EmStandardPhysics():         default (option 0) for photon transport (e.g., gamma spectroscopy examples)
    // G4EmStandardPhysics_option4(): recommended for alpha particles and low-energy charged particles,
    //                                as it includes the most accurate EM models available in Geant4
    
    emPhysicsList       = new G4EmStandardPhysics();         // Use G4EmStandardPhysics_option4() for alpha particles!!!
    decPhysicsList      = new G4DecayPhysics();
    radDecayPhysicsList = new G4RadioactiveDecayPhysics();

    // ::: Register Physics Processes :::
    RegisterPhysics(new G4EmStandardPhysics());             // ElectroMagnetic (EM) Physics
    RegisterPhysics(new G4RadioactiveDecayPhysics());       // Decay Phyics
    RegisterPhysics(new G4DecayPhysics());

}

// ::::::::::::::::::::::::::::::::
// :::  Destructor definition   :::
// ::::::::::::::::::::::::::::::::
PhysicsList::~PhysicsList()
{
    delete decPhysicsList;
    delete radDecayPhysicsList;
    delete emPhysicsList;
}

// ::::::::::::::::::::::::::::::::
// :::  Constructing Particles  :::
// ::::::::::::::::::::::::::::::::
void PhysicsList::ConstructParticle() 
{
  decPhysicsList->ConstructParticle();
}

// ::::::::::::::::::::::::::::::::
// :::  Constructing Processes  :::
// ::::::::::::::::::::::::::::::::
void PhysicsList::ConstructProcess()
{
  AddTransportation();
  emPhysicsList->ConstructProcess();
  decPhysicsList->ConstructProcess();
  radDecayPhysicsList->ConstructProcess();
}

void PhysicsList::SetCuts() {
  // Definition of  threshold of production
  // of secondary particles
  // This is defined in range.
  defaultCutValue = 0.1*mm;

  SetCutValue(0.1*mm, "gamma");
  SetCutValue(0.1*mm, "e-");
  SetCutValue(0.1*mm, "e+");
  SetCutValue(1.0*mm, "alpha");


  // By default the low energy limit to produce
  // secondary particles is 990 eV.
  // This value is correct when using the EM Standard Physics.
  // When using the Low Energy Livermore this value can be
  // changed to 250 eV corresponding to the limit
  // of validity of the physics models.
  // Comment out following three lines if the
  // Standard electromagnetic Package is adopted.
  //Low originally set to 100eV
  G4double lowLimit = 1. * keV;
  G4double highLimit = 100. * GeV;

  G4ProductionCutsTable::GetProductionCutsTable()->SetEnergyRange(lowLimit,
                                                                  highLimit);

  // Print the cuts
  if (verboseLevel>0) DumpCutValuesTable();
}