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
    emPhysicsList       = new G4EmStandardPhysics();
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
  defaultCutValue = 0.004*mm; //0.03
  SetCutValue(0.001*mm, "alpha");
  SetCutValue(defaultCutValue, "e-");
  SetCutValue(defaultCutValue, "e+");


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