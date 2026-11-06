// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::        Source file for Stacking Action        :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries
#include "StackingAction.hh"
#include "G4VProcess.hh"
#include "G4ios.hh"


// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

StackingAction::StackingAction(): isDaRTSimulation(false)
{}


// ::::::::::::::::::::::::::::::::
// :::  Destructor definition   :::
// ::::::::::::::::::::::::::::::::

StackingAction::~StackingAction()
{}


G4ClassificationOfNewTrack StackingAction::ClassifyNewTrack(const G4Track * aTrack)
{
    G4ParticleDefinition *Particle = aTrack   -> GetDefinition();     
    G4String                  Name = Particle -> GetParticleName();   
                    classification = fUrgent;                         

    /*
     * fUrgent   = Track is placed in the urgent stack
     * fWaiting  = Track waits until the urgent stack is empty
     * fPostpone = Track is postponed to the next event
     * fKill     = Track is deleted immediately
     */

    // If this is the primary radioactive nucleus
    if (aTrack->GetParentID() == 0)
    {
        if      (Name == "Ra224") {isDaRTSimulation = true;}
        else if (Name == "Am241") {isDaRTSimulation = false;}
    }

    // ::::::::::::::::::::::::::::::::
    // :::           DaRT           :::
    // ::::::::::::::::::::::::::::::::
    if (isDaRTSimulation)
    {
        if (aTrack->GetParentID() != 0)
        {
            // Kill all alpha particles
            if (Name == "alpha" || Name == "anti_nu_e")  {classification = fKill;}

            // Kill only electrons produced directly by radioactive decay
            else if (Name == "e-" && aTrack->GetCreatorProcess() != nullptr)
            {
                G4String ProcessName = aTrack->GetCreatorProcess()->GetProcessName();

                if (ProcessName == "RadioactiveDecay") {classification = fKill;}
            }

        }
    }

    // :::::::::::::::::::::::::::::::
    // :::         Am-241          :::
    // :::::::::::::::::::::::::::::::
    else
    {
        if (Name == "Np237")  {classification = fKill;}
    }

    // :::::::::::::::::::::::::::::::::::::::::::::::
    // :::      Print track information            :::
    // :::::::::::::::::::::::::::::::::::::::::::::::
/*
    G4String ProcessName;

    if (aTrack->GetCreatorProcess() == nullptr)
    {
        ProcessName = "Primary";
    }
    else
    {
        ProcessName = aTrack->GetCreatorProcess()->GetProcessName();
    }

    G4String TrackStatus;

    if      (classification == fKill)     {TrackStatus = "KILLED";}
    else if (classification == fUrgent)   {TrackStatus = "NOT KILLED";}
    else if (classification == fWaiting)  {TrackStatus = "WAITING";}
    else if (classification == fPostpone) {TrackStatus = "POSTPONED";}

    G4cout
        << "Particle: "  << Name
        << " | Process: " << ProcessName
        << " | Parent ID: " << aTrack->GetParentID()
        << " | Track ID: " << aTrack->GetTrackID()
        << " | Status: " << TrackStatus
        << G4endl;
*/
    return classification;
}