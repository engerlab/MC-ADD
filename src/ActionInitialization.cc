// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::     Source file for Action Initialization     :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries
#include "ActionInitialization.hh"


// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

ActionInitialization::ActionInitialization()
{}


// ::::::::::::::::::::::::::::::::
// :::   Destructor definition  :::
// ::::::::::::::::::::::::::::::::

ActionInitialization::~ActionInitialization()
{}


void ActionInitialization::BuildForMaster() const
{
    RunAction        *runAction = new RunAction(); // Important to add it here too because the histogram will be created in the master thread
    SetUserAction(runAction);
}

void ActionInitialization::Build() const
{
    PrimaryGenerator      *generator = new PrimaryGenerator();  // We hand over PrimaryGenerator
    RunAction             *runAction = new RunAction();
    StackingAction   *stackingAction = new StackingAction();

    // We set the objects (*object)
    SetUserAction(generator);
    SetUserAction(runAction);
    SetUserAction(stackingAction);
}