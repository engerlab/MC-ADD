// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::        Source file for Stacking Action        :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries
#include "StackingAction.hh"


// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

StackingAction::StackingAction()
{}


// ::::::::::::::::::::::::::::::::
// :::  Destructor definition   :::
// ::::::::::::::::::::::::::::::::

StackingAction::~StackingAction()
{}


G4ClassificationOfNewTrack StackingAction::ClassifyNewTrack(const G4Track * aTrack)
{
    G4ParticleDefinition *Particle = aTrack   -> GetDefinition();     // We get the particle definition
    G4String                  Name = Particle -> GetParticleName();   // The particle name
                    classification = fUrgent;                         // We classifiy the stacks as Wating


    /* Classifications:
     * fUrgent   = All tracks are put into the urgent stack, let's say in a "priority" stack
     * fWaiting  = Once the Urgent stack is empty, all the tracks that were put into the waiting stack will be sent into the Urgent stack
     * fPostpone = The track will be postponed to the next event
     * fKill     = The track is deleted immediately and not stored in any stack.
     */

    // If this is a primary particle (i.e., the radioactive nucleus itself)
    if (aTrack->GetParentID() == 0)
    {
        if (Name == "Ra224")       {isDaRTSimulation = true;}
        else if (Name == "Am241")  {isDaRTSimulation = false;}
    }

    // ::::::::::::::::::::::::::::::::
    // :::           DaRT           :::
    // ::::::::::::::::::::::::::::::::
    if (isDaRTSimulation)
    {
        if (aTrack->GetParentID() != 0)                          // If it's a secondary particle
        {
           if (Name =="alpha") {classification = fUrgent;}  
           else {classification = fKill;}
        }
    }

   

    // :::::::::::::::::::::::::::::::
    // :::         Am-241          :::
    // :::::::::::::::::::::::::::::::
    else
    {
        if (Name == "Np237") {classification = fKill;}  // Kill Np-237 since it's an extremelly long-lived radionuclide and its radioactive products are never seen experimentally    
    }

    return classification;
}