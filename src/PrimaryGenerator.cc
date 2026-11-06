// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::       Source file for Primary Generator       :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries
#include "PrimaryGenerator.hh"



// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

PrimaryGenerator::PrimaryGenerator()
{
    fParticleGun = new G4GeneralParticleSource();

    /*
    fParticleGun = new G4ParticleGun(1);  // 1 is defined for 1 particle per event

    // ::: Particle gun position :::
    G4double X = 0.*m;
    G4double Y = 0.*m;
    G4double Z = 0.*m;

    G4ThreeVector pos(X, Y, Z);

    // ::: Particle Direction :::
    G4double pX = 0.;
    G4double pY = 0.;
    G4double pZ = 1.;

    G4ThreeVector mom(pX, pY, pZ); // Momentum

    

    // ::: Set arguments to particle gun :::
    fParticleGun->SetParticlePosition(pos);
    fParticleGun->SetParticleMomentumDirection(mom);
    */
    
}


// ::::::::::::::::::::::::::::::::
// :::  Destructor definition   :::
// ::::::::::::::::::::::::::::::::

PrimaryGenerator::~PrimaryGenerator()
{
    delete fParticleGun;     // We have to delete it to free memory
}


// ::::::::::::::::::::::::::::::::
// :::   Functions definition   :::
// ::::::::::::::::::::::::::::::::

void PrimaryGenerator::GeneratePrimaries(G4Event *anEvent)
{
    // ::: Create Vertex :::
    fParticleGun->GeneratePrimaryVertex(anEvent);    // The particle gun generates a vertex (function tat shoots the particle), and we have to hand over the event to fParticleGun
}