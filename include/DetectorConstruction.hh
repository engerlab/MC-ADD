// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::     Header file for Detector Construction     :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

#ifndef DETECTORCONSTRUCTION_HH
#define DETECTORCONSTRUCTION_HH

// Include needed libraries
#include "G4VUserDetectorConstruction.hh" // Main class from which we will inherit
#include "G4Box.hh"                       // Geometry libraries for the construction. This is a solid volume, deals with the geometry of the volume
#include "G4Sphere.hh"
#include "G4Tubs.hh"
#include "G4RotationMatrix.hh"            // To rotate .stl .obj geometries
#include "G4Transform3D.hh"
#include "G4LogicalVolume.hh"             // Geometry library for logical volumes. Takes the solid volume and assings materials to it
#include "G4VPhysicalVolume.hh"           // Geometry library for physical volumes.
#include "G4PVPlacement.hh"
#include "G4ThreeVector.hh"               // Deals with the position
#include "G4Material.hh"                  // Library for materials
#include "G4NistManager.hh"               // To use the materials, we need to inclde the NIST manager as well
#include "G4SystemOfUnits.hh"             // Library to use units like m, ev, etc.
#include "G4UnitsTable.hh"

#include "G4VisAttributes.hh"             // Attributes for visualization
#include "G4Color.hh"
#include "G4SDManager.hh"

#include "SensitiveDetector.hh"           // Sensitive Detector user class

// ::::::::::::::::::::::::::::::::
// :::    Class definition      :::
// ::::::::::::::::::::::::::::::::

class DetectorConstruction : public G4VUserDetectorConstruction  // We name our own class "DetectorConstruction" inherited from G4VUserDetectorConstruction
{
public:
    DetectorConstruction();
    virtual ~DetectorConstruction();            // We use virtual because the destructor (in this case) is already defined in G4VUserDetectorConstruction. So, it will be overwritten

    virtual G4VPhysicalVolume *Construct();   // Main function that takes over the construction of the detector


    // We can define the Solid, Logical, and physical volumes variables here (Just to make the source code more neat)

    // ::: Solids :::
    G4Box    *World,
          *Detector;

    G4Sphere *Source;

    G4LogicalVolume        *World_log,  // Logical volume
                          *Source_log;
                          
    G4VPhysicalVolume     *World_phys,  // World
                       *Detector_phys,  // Detector
                         *Source_phys;  // Source


    // ::: Position :::
    G4ThreeVector Pos1,  // World and Source
                  Pos2,  // Source
                  Pos3;  // Detector

private: // We want to access the detector outside the contruct function 

    // For rotatting volumes
    G4RotationMatrix  *Rotation;
    //G4Transform3D    *transform;

    G4LogicalVolume      *Detector_log; // logical volume

    virtual void ConstructSDandField(); // Important function that will construct any Sensitive Detector or Field (e.g. Magnetic Field)

};

#endif