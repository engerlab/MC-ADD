// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::        Header file for Physics List           :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

#ifndef PHYSICSLIST_HH
#define PHYSICSLIST_HH

// Include needed libraries
#include "G4VModularPhysicsList.hh"     // Main class from which we will inherit
#include "G4EmStandardPhysics.hh"       // Standard Physics list for electromagnetic interactions
#include "G4RadioactiveDecayPhysics.hh" // To handle radioactive decay
#include "G4DecayPhysics.hh"
#include "G4EmConfigurator.hh"
#include "G4SystemOfUnits.hh"             // Library to use units like m, ev, etc.
#include "G4UnitsTable.hh"
#include "globals.hh"

// ::::::::::::::::::::::::::::::::
// :::    Class definition      :::
// ::::::::::::::::::::::::::::::::

class PhysicsList : public G4VModularPhysicsList  // We name our own class "PhysicsList" inherited from ModularPhysicsList
{
public: 
    PhysicsList();   // Constructor
    ~PhysicsList();  // Destructor

    void ConstructParticle();
    void ConstructProcess();

protected:

  void SetCuts();

private:
  G4VPhysicsConstructor* emPhysicsList;
  G4VPhysicsConstructor* decPhysicsList;
  G4VPhysicsConstructor* radDecayPhysicsList;
};

#endif