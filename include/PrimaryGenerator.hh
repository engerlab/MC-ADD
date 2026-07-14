// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::      Header file for Primary Generator        :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

#ifndef PRIMARYGENERATOR_HH
#define PRIMARYGENERATOR_HH

// Include needed libraries
#include "G4VUserPrimaryGeneratorAction.hh"  // Main class from which we will inherit
#include "G4ParticleDefinition.hh"           // Library that contains the names of the particles (e.g. e-, e+, alphas, gammas, etc)
#include "G4ParticleGun.hh"                  // Library to shoot particles (or beams)
#include "G4ParticleTable.hh"
#include "G4GeneralParticleSource.hh"
#include "G4SystemOfUnits.hh"                // Library to use units such as eV
#include "G4IonTable.hh"                     // Library to access the ions available in Geant4


// ::::::::::::::::::::::::::::::::
// :::    Class definition      :::
// ::::::::::::::::::::::::::::::::

class PrimaryGenerator : public  G4VUserPrimaryGeneratorAction
{
public: 
    PrimaryGenerator();   // Constructor
    ~PrimaryGenerator();  // Destructor

    virtual void GeneratePrimaries(G4Event *);   // We are overwritting a function that already exists

private:
    G4GeneralParticleSource *fParticleGun;       // We define a private variable/object for the particle source

};

#endif