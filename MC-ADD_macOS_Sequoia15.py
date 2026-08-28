# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                                                                                                          :::
# :::                                           MC-ADD Graphical User Interface                                                :::
# :::                                                   macOS Sequoia 15.6                                                     :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# This Python script generates the GUI for the MC-ADD app. This script is divided into 2 main sections:
#   
#   1) Collecting Input Information: This section defines the variables used to store the user's input along with the text 
#                                    templates required to generate both the DetectorConstruction.cc file and the macro file, 
#                                    which contain the user-defined geometry.
#   
#   2) GUI: This section generates the GUI itself, including all the corresponding text fields and input options for the user to 
#           define the geometry.
# 
# Important Notes!: 
#       - This GUI is NOT the DetectorConstruction.cc file or macro file! If you modify anything in the code, it may result in 
#         errors during your simulations. If you wish to modify the geometry, please follow the instructions in 
#         DetectorConstruction.cc itself. 
#       
#       - This GUI limits the world, radioactive source, and detector to the following:
#                           - World: Box-shaped (2x2x2 m³) with the possibility to choose between Air and Water as the material.
#                           - Source and Detector: Both shapes are limited to box and cylindrical shapes, with the option to 
#                                                  select any material from the Geant4 materials database.
#                                                  The source is limited to Am-241 and Ra-224. If you wish to define 
#                                                  a new source, check the Geant4 documentation for guidance. 
#       
#       - For Mesh geometries, they must be defined in their respective field with their exact names, separated by commas.
#         If a Mesh geometry is added, then make sure you uncoment such geometry and to define their materials!!
#       - After defining all new geometries and clicking "Save," the GUI will generate the DetectorConstruction.cc file, 
#         the macro file, and a .txt version of DetectorConstruction.cc. All these files will be saved in their respective 
#         folders to avoid errors.
#       - If you already saved your geometry and wish to re-define it with the same name you used to save it. You can either 
#         modify the DetectorConstruction.cc file directly or just run the GUI again. For the latter you must delete the 
#         generated txt file located in the DetectorConstructionGeometries folder
#            
# Author: Víctor Daniel Díaz Martínez
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# :::::: We import the needed libraries ::::::
import tkinter as tk
import shutil
import os
from tkinter import ttk, filedialog, messagebox

# ::: Important paths for sending the .cc, .txt, and macro files to their respective folders :::
# ::: macOS Sequoia 15.6 :::
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                                  # Obtaining the main path (same level where this script should be)
SourceCCFile       = os.path.join(BASE_DIR, "DetectorConstruction.cc")                 # Path where the GUI-generated DetectorConstruction.cc file is located
DestinationCCFile  = os.path.join(BASE_DIR, "src", "DetectorConstruction.cc")          # Path where the old DetectorConstruction.cc file will be replaced with the GUI-generated one
DestinationTxtFile = os.path.join(BASE_DIR, "DetectorConstructionGeometries")          # Path to the folder where .txt version of the GUI-generated DetectorConstruction files will be stored
os.makedirs(DestinationTxtFile, exist_ok=True)                                         # Command to create the DetectorConstructionGeometries folder if it does not exist


# ::: For loading previous geometries (to be added):::
#GEOMETRY_FOLDER = "DetectorConstructionGeometries"                                        # Folder containing txt files
#DESTINATION_FOLDER = "src"                                                                # Folder where DetectorConstruction.cc is located
#DESTINATION_FILE = os.path.join(DESTINATION_FOLDER, "DetectorConstruction.cc")


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                                                :::
# :::   C O L L E C T I N G    I N P U T    I N F O R M A T I O N    :::
# :::                                                                :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def save_input():

    # :::::: Collecting user inputs from dropdown menus ::::::

    # The following lines retrieve the user's information regarding:

    # ::: Shape (box or cylinder):::
    source_choice   = source_combobox.get()                                                   # Get the selected shape from Source dropdown
    detector_choice = detector_combobox.get()                                                 # Get the selected shape from Detector dropdown

    # ::: Materials ::: 
    world_material    = world_material_combobox.get()                                         # Get the selected material from World dropdown
    source_material   = source_material_combobox.get()                                        # Get the selected material from Source dropdown
    detector_material = detector_material_combobox.get()                                      # Get the selected material from Detector dropdown

    # ::: Dimension and Position :::
    source_dim_values   = [source_dim1.get(), source_dim2.get(), source_dim3.get()]           # Get numerical values for the Source's dimension: x,y,z or r1,r2, length
    detector_dim_values = [detector_dim1.get(), detector_dim2.get(), detector_dim3.get()]     # Get numerical values for the Detector's dimension: x,y,z or r1,r2, length

    source_pos_values   = [source_pos1.get(), source_pos2.get(), source_pos3.get()]           # Get numerical values for the Source's position
    detector_pos_values = [detector_pos1.get(), detector_pos2.get(), detector_pos3.get()]     # Get numerical values for the Detector's position


    # ::: Mesh files names :::
    CADinput_names  = CAD_Input.get()                                                         # Stores the raw input as a single string.
    CADfile_names   = [name.strip() for name in CADinput_names.split(',') if name.strip()]    # Processes the input
    CAD_Folder_Path = CAD_Folder_Input.get()                                                  # Stores the path to the folder containing the Mesh files

    # ::: MacroFile :::
    Radionuclide = radionuclide_combobox.get()                                                # Dropdown menu for the radionuclide: Am-241 or DaRT
    Location_source = radionuclide_location_combobox.get()                                    # Location of the atoms on the source: Volume or Surface
    Runs_input = RunsInput.get()                                                              # Number of runs

    # ::: Naming the Geometry :::
    geometryName = GeometryName.get()                                                         # Name of the geometry (e.g. PlasticScintillatorGeometry, LYSOGeometry)


    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    

    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::                                                                :::
    # :::          D E T E C T O R    C O N S T R U C T I O N.CC         :::
    # :::                                                                :::
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    with open("DetectorConstruction.cc", "w") as file:                                        # Save the user's input to a text file


        # :::::: Detector Construction Template ::::::
        file.write(f"""// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::     Source file for Detector Construction     :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries
#include "DetectorConstruction.hh"
#include "CADMesh.hh"               // To import Mesh files


// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

DetectorConstruction::DetectorConstruction()
{{}}


// ::::::::::::::::::::::::::::::::
// :::  Destructor definition   :::
// ::::::::::::::::::::::::::::::::

DetectorConstruction::~DetectorConstruction()
{{}}


// ::::::::::::::::::::::::::::::::::
// ::: Physical volume definition :::
// :::        (function)          :::
// ::::::::::::::::::::::::::::::::::

G4VPhysicalVolume *DetectorConstruction::Construct()
{{ 
    G4bool checkOverlaps = true;                                 // Command to check for geometries overlaps

    G4NistManager  *nist = G4NistManager::Instance();             // Nist manager includes several materials that we can use


    // ::::::::::::::::::::::::::::::::
    // :::          Elements        :::
    // ::::::::::::::::::::::::::::::::
    G4Element*  Lu = nist->FindOrBuildElement("Lu");
    G4Element*  Y  = nist->FindOrBuildElement("Y");
    G4Element*  Si = nist->FindOrBuildElement("Si");
    G4Element*  O  = nist->FindOrBuildElement("O");
    G4Element*  Ce = nist->FindOrBuildElement("Ce");
    G4Element*  Fe = nist->FindOrBuildElement("Fe");
    G4Element*  Cr = nist->FindOrBuildElement("Cr");
    G4Element*  N  = nist->FindOrBuildElement("N");
    G4Element*  Ni = nist->FindOrBuildElement("Ni");
    G4Element*  Mn = nist->FindOrBuildElement("Mn");
    G4Element*  C  = nist->FindOrBuildElement("C");
    G4Element*  S  = nist->FindOrBuildElement("S");
    G4Element*  P  = nist->FindOrBuildElement("P");
    G4Element*  Cu = nist->FindOrBuildElement("Cu");
    G4Element*  Mo = nist->FindOrBuildElement("Mo");
    G4Element*  H = nist->FindOrBuildElement("H");
    

    // ::::::::::::::::::::::::::::::::
    // :::        Materials         :::
    // ::::::::::::::::::::::::::::::::
    G4Material *WorldMat = nist->FindOrBuildMaterial("{world_material}");   // We name and define a material from the nist manager. For other materials refer to the Geant4 Material Database
    G4Material    *PbMat = nist->FindOrBuildMaterial("G4_Pb");  
    G4Material   *SrcMat = nist->FindOrBuildMaterial("{source_material}");    // Source's material
    G4Material   *DetMat = nist->FindOrBuildMaterial("{detector_material}");  // Detector's Active Volume material
    G4Material   *Water = nist->FindOrBuildMaterial("G4_WATER"); 
    G4Material   *PMMA  = nist->FindOrBuildMaterial("G4_PLEXIGLASS"); 


    // ::::::::::::::::::::::::::::::::::::::::::
    // :::  User-defined materials/compounds  :::
    // ::::::::::::::::::::::::::::::::::::::::::

    // To define a new material use the following commands:
    //          G4Material("Name", Density*g/cm3, No. of elements)
    //          Name->AddElement(Element, No of atoms);  // Define the number of elements and the atom numbers for each element

    // :::::::::::::::::::::::::::
    // :::  Examples provided  :::
    // :::::::::::::::::::::::::::

    // :::::::: LYSO ::::::::
    G4Material* LYSO = new G4Material("LYSO", 7.1*g/cm3, 5);
    LYSO->AddElement(Lu, 2);
    LYSO->AddElement( Y, 2);
    LYSO->AddElement(Si, 1);
    LYSO->AddElement( O, 5);
    LYSO->AddElement(Ce, 1);

    // :::::::: Stainless steel 316LVM ::::::::
    // Values retrieved from: https://www.ulbrich.com/alloys/316lvm-stainless-steel-uns-s31673/
    // You can also define a material defining the % of each element. The % must add up 1
    G4Material* StainlessSteel = new G4Material( "SSteel_316LVM", 7.92*g/cm3, 11 );
    StainlessSteel->AddElement( C , 0.0003 ); // 0.03%
    StainlessSteel->AddElement( P , 0.0003 ); // 0.03%
    StainlessSteel->AddElement( Si, 0.0075 ); // 0.75%
    StainlessSteel->AddElement( Ni, 0.13   ); // 13.0%
    StainlessSteel->AddElement( Cu, 0.0005 ); // 0.05%
    StainlessSteel->AddElement( Mn, 0.02   ); // 2.00%
    StainlessSteel->AddElement( S,  0.0001 ); // 0.01%
    StainlessSteel->AddElement( Cr, 0.17   ); // 17.0%
    StainlessSteel->AddElement( Mo, 0.0225 ); // 2.25%
    StainlessSteel->AddElement( N , 0.0010 ); // 0.10%
    StainlessSteel->AddElement( Fe, 0.6478 ); // Balance (64.78%)

    // :::::::: Pebax C2H40 ::::::::
    G4Material* pebax = new G4Material( "Pebax", 1.01*g/cm3, 3 );
    pebax->AddElement( C , 2 );
    pebax->AddElement( H , 4 );
    pebax->AddElement( O , 1 );

    // :::::::: Silicone ::::::::
    G4Material* silicone = new G4Material( "silicone", 1.1*g/cm3, 4 );
    silicone->AddElement( C , 2 );
    silicone->AddElement( H , 6 );
    silicone->AddElement( Si, 1 );
    silicone->AddElement( O , 1 );

    // :::::::: Silicone Grease ::::::::
    G4Material* OpticalGreaseMat = new G4Material( "OpticalGreaseMat", 1.1*g/cm3, 4 );
    OpticalGreaseMat->AddElement( C , 2 );
    OpticalGreaseMat->AddElement( H , 6 );
    OpticalGreaseMat->AddElement( Si, 1 );
    OpticalGreaseMat->AddElement( O , 1 );

    // :::::::: Polyether Ether Ketona (PEEK,C19H12O3) ::::::::
    G4Material* PEEK = new G4Material( "PEEK", 1.32*g/cm3, 3 );
    PEEK->AddElement( C , 19 );
    PEEK->AddElement( H , 12 );
    PEEK->AddElement( O , 3  );


    // ::::::::::::::::::::::::::::::::
    // :::         Geometry         :::
    // ::::::::::::::::::::::::::::::::
    
    // :::  Positions  :::
    Pos1 = G4ThreeVector(0, 0, 0);  // World position
    Pos2 = G4ThreeVector({source_pos_values[0]}*mm, {source_pos_values[1]}*mm, {source_pos_values[2]}*mm);  // Source
    Pos3 = G4ThreeVector({detector_pos_values[0]}*mm, {detector_pos_values[1]}*mm, {detector_pos_values[2]}*mm);  // Detector


    // :::::::::::::::::::
    // :::::: World ::::::
    // :::::::::::::::::::

    // ::: Dimensions :::
    G4double WorldX = 2./2*m; // Geant4 always takes half of the length. Therefore define them as X/2 or X*0.5
    G4double WorldY = 2./2*m;
    G4double WorldZ = 2./2*m;

    World      = new G4Box("World", WorldX, WorldY, WorldZ); // Solids deals with the definition of the shapes
    World_log  = new G4LogicalVolume(World, WorldMat, "World_log");
    World_phys = new G4PVPlacement(0, Pos1, World_log, "World_phys", 0, false, 0, checkOverlaps); // The first 0 means rotation. The world does not need to be rotated so, = 0. 
                                                                                                  // The second 0 means if this volume is a daughter (aka. if it is inside another volume). In this case, No.
                                                                                                  // The third 0 means the copy number.

    // ::::::::::::::::::::::
    // ::::::  Source  ::::::
    // ::::::::::::::::::::::

    Rotation = new G4RotationMatrix();    // A rotation is defined to align all the source geometry in the Y axis direction
    Rotation->rotateX(90.*deg);
    Rotation->rotateY(0.*deg);
    Rotation->rotateZ(0.*deg);
""")

        # :::::: Dimensions of the source based on the Shape ::::::
        if source_choice == "Box":                          # For Box
            file.write(f"""
    G4double SourceX = {source_dim_values[0]}/2.*mm;
    G4double SourceY = {source_dim_values[1]}/2.*mm;
    G4double SourceZ = {source_dim_values[2]}/2.*mm;

    G4Box      *Source = new G4Box("Source", SourceX, SourceY, SourceZ);
            Source_log = new G4LogicalVolume(Source, SrcMat, "Source_log");
           Source_phys = new G4PVPlacement(0, Pos2, Source_log, "Source_phys", World_log, false, checkOverlaps);
            """)

        elif source_choice == "Cylinder":                   # For Cylinder
            file.write(f"""
    G4double SourceInRad     = {source_dim_values[0]}*mm;
    G4double SourceOutRad    = {source_dim_values[1]}*mm;
    G4double SourceThickness = {source_dim_values[2]}/2.*mm;

    G4Tubs   *Source  = new G4Tubs("Source", SourceInRad, SourceOutRad, SourceThickness, 0.*deg, 360*deg);
          Source_log  = new G4LogicalVolume(Source, SrcMat, "Source_log");
          Source_phys = new G4PVPlacement(Rotation, Pos2, Source_log, "Source_phys", World_log, 0, checkOverlaps);
            """)

        # :::::: Dimensions of the detector based on the Shape ::::::
        if detector_choice == "Box":                          # For Box
            file.write(f"""
    
    // ::::::::::::::::::::::
    // :::::: Detector ::::::
    // ::::::::::::::::::::::

    G4double DetectorX = {detector_dim_values[0]}/2.*mm;
    G4double DetectorY = {detector_dim_values[1]}/2.*mm;
    G4double DetectorZ = {detector_dim_values[2]}/2.*mm;

    Detector      = new G4Box("Detector", DetectorX, DetectorY, DetectorZ);
    Detector_log  = new G4LogicalVolume(Detector, DetMat, "Detector_log");
    Detector_phys = new G4PVPlacement(0, Pos3, Detector_log, "Detector_phys", World_log, false, checkOverlaps);
            """)

        elif detector_choice == "Cylinder":                   # For Cylinder
            file.write(f"""

    // ::::::::::::::::::::::
    // :::::: Detector ::::::
    // ::::::::::::::::::::::

    G4double DetInnerRadius = {detector_dim_values[0]}*mm;
    G4double DetOuterRadius = {detector_dim_values[1]}*mm;
    G4double DetThickness   = {detector_dim_values[2]}/2.*mm;

    G4Tubs   *Detector  = new G4Tubs("Detector", DetInnerRadius, DetOuterRadius, DetThickness, 0.*deg, 360*deg);
          Detector_log  = new G4LogicalVolume(Detector, DetMat, "Detector_log");
          Detector_phys = new G4PVPlacement(0, Pos3, Detector_log, "Detector_phys", World_log, 0, checkOverlaps);
            """)

        file.write(f"""
        
    // ::::::::::::::::::::::::::::::::::::::
    // :::          Mesh Geometries        :::
    // ::::::::::::::::::::::::::::::::::::::

    /* In this section you can add more geometries using Mesh files in .obj or .stl format.
     * !!! Coppy and uncomment the following section if you want to model the Mesh files, or if you wich to add more Mesh geometries. !!!
     * !!! The 'X' represents the number of Mesh geometries, 'Name' is the name of the Mesh file, and 'MATERIAL' should be defined before compiling. !!!
     *
     * The Mesh files are added throught the GUI, but if you wish to add them manually, here is the detailed processs on how to proceed:
     *     1) Import .obj, or .stl geometry using:
     *
     *        auto meshX = CADMesh::TessellatedMesh::FromOBJ("NAME.obj");  // If you want to add more Mesh files, keep using mesh2,3,4, etc. Remember to write the correct file name!
     *        auto meshx = CADMesh::TessellatedMesh::FromSTL("Name.stl");  // stl geometries MUST BE SAVED IN ASCII STL
     *
     *     2) Scale the geoemtry. Recommended to set it to 1 to keep your original dimensions
     *
     *        meshX->SetScale(1); // For more geoemtries use mesh2, mesh3, etc.
     *
     *     3) Setting an offset in the geoemtry position. Modify it as needed, but adding mesh2, mesh3, etc for more geometries.
     *
     *        meshX->SetOffset(x, y, z);
     *        meshX->SetOffset(G4ThreeVector(x, y, z));
     *
     *     4) Assigning names and materials. Replace NAME for the name of your geometry (e.g.  NAME --> Shielding).
     *                                       Replace MATERIAL with your defined material (e.g. MATERIAL --> LYSO).
     *
     *        // ::: Name :::
     *        auto NAME     = meshX->GetSolid();                                      
     *        auto NAME_log = new G4LogicalVolume(NAME, MATERIAL, "NAME_log",0,0,0);
     *                        new G4PVPlacement(rotation, Pos1, "NAME", NAME_log, World_log, false, 0, false);
     * 
     * Credits to Christopher Poole for this section (https://github.com/christopherpoole/CADMesh/tree/master)
     */

    G4double x = 0.0; // Do not comment this line.
    G4double y = 0.0; // Do not comment this line.
    G4double z = 0.0; // Do not comment this line.
    
    /*  // :::::::::::: UNCOMMENT THE FOLLOWING SECTION STARTING FROM HERE UP TO ....
    //std::string basePath = "{CAD_Folder_Path}/Obj/";  // For .obj files
    //std::string basePath = "{CAD_Folder_Path}/Stl/";  // For .stl files. MUST BE IN ASCII STL

       """)

        for i, CADfile_name in enumerate(CADfile_names, start=1):
                    file.write(f"""
    // ::: {CADfile_name} :::
    //auto mesh{i} = CADMesh::TessellatedMesh::FromOBJ(basePath + "{CADfile_name}.obj");
    //auto mesh{i} = CADMesh::TessellatedMesh::FromSTL(basePath + "{CADfile_name}.stl");

    mesh{i}->SetScale(1);
    mesh{i}->SetOffset(x, y, z);
    mesh{i}->SetOffset(G4ThreeVector(x, y, z));

    Rotation = new G4RotationMatrix();
    Rotation->rotateX(0.*deg);
    Rotation->rotateY(0.*deg);
    Rotation->rotateZ(0.*deg);

    auto {CADfile_name} = mesh{i}->GetSolid();
    auto {CADfile_name}_log = new G4LogicalVolume({CADfile_name}, MATERIAL, "{CADfile_name}_log", 0, 0, 0);
                        new G4PVPlacement(Rotation, Pos1, {CADfile_name}_log, "{CADfile_name}", World_log, 0, checkOverlaps);
            """)          


        file.write(f"""

    */  // ... UP TO HERE! 


    // ::::::::::::::::::::::::::::::::::::::
    // :::    Visualisation Attributes    :::
    // ::::::::::::::::::::::::::::::::::::::

    // Add your CAD_log volumes here for visualization too

    // ::: Detector :::
    G4VisAttributes *DetVisAtt = new G4VisAttributes(G4Color(0.0, 0.0, 1.0, 0.5)); // Blue
    DetVisAtt->SetForceSolid(true);
    Detector_log->SetVisAttributes(DetVisAtt);

    // ::: Source :::
    G4VisAttributes *SrcVisAtt = new G4VisAttributes(G4Color(1.0, 0.0, 0.0, 0.5)); // Red
    SrcVisAtt->SetForceSolid(true);
    Source_log->SetVisAttributes(SrcVisAtt);


    return World_phys;  // Always return the physical World
}}


// ::::::::::::::::::::::::::::::::::
// :::    Sensitive Detector      :::
// :::         function           :::
// ::::::::::::::::::::::::::::::::::

void DetectorConstruction::ConstructSDandField()
{{
    SensitiveDetector *sensDet = new SensitiveDetector("SensitiveDetector");
    Detector_log->SetSensitiveDetector(sensDet);
    G4SDManager::GetSDMpointer()->AddNewDetector(sensDet);
}}

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::: End ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        """)
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::    Saving the DetectorCosntruction.cc into .txt    :::
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    with open("DetectorConstruction.cc", "r") as cc_file:     # Opening and reading the .cc file
        ccContent = cc_file.read()

    with open(geometryName +".txt", "w") as txt_file:         # Saving it as a txt file
        txt_file.write(ccContent)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                                                :::
# :::       L O A D    P R E V I O U S    G E O M E T R I E S        :::
# :::                                                                :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# !!!!!!!!!!!!!!!!! FEATURE TO BE ADDED !!!!!!!!!!!!!!!
#        def load_geometry():
#            # Step 1: Open file dialog in the specific folder
#            txt_file = filedialog.askopenfilename(
#                initialdir=GEOMETRY_FOLDER,  # Open correct folder
#                title="Select a Geometry File",
#                filetypes=[("Text Files", "*.txt")]  # Only allow .txt files
#                )
                
#            if not txt_file:  # If user cancels, do nothing
#                return
                
#            # Step 2: Read the selected file’s content
#            with open(txt_file, "r") as file:
#                content = file.read()
                    
#            # Step 3: Ensure the destination folder exists        
#            if not os.path.exists(DESTINATION_FOLDER):
#                os.makedirs(DESTINATION_FOLDER)

#            # Step 4: Overwrite DetectorConstruction.cc with the new content
#            with open(DESTINATION_FILE, "w") as file:
#                file.write(content)

#            # Step 5: Show success message
#            messagebox.showinfo("Success", f"Geometry loaded successfully into {DESTINATION_FILE}")



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                                                :::
# :::                     M A C R O    F I L E                       :::
# :::                                                                :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# :::::: Converting the source and detector values into float ::::::
    # :::::: Source ::::::
    halfx = float(source_dim_values[0]) / 2
    halfy = float(source_dim_values[1]) / 2
    halfz = float(source_dim_values[2]) / 2

    # :::::: Detector ::::::
    # ::: Box :::
    DetX = float(detector_dim_values[0]) / 2
    DetY = float(detector_dim_values[1]) / 2
    DetZ = float(detector_dim_values[2]) / 2

    voxX = float(detector_dim_values[0]) / 0.01 
    voxY = float(detector_dim_values[1]) / 0.01 
    voxZ = float(detector_dim_values[2]) / 0.01

    # ::: Cylinder :::
    DetLen = float(detector_dim_values[2]) / 2

    # Voxels
    iR = float(detector_dim_values[1]) / 0.01
    iPhi = 360
    iZ = float(detector_dim_values[2]) / 0.01
    cylinderVis = iZ - 1


# :::::: Define radionuclide properties ::::::
# MOST COMMON RADIOISOTOPES USED ONLY!!!!!
    radionuclides = {
        # ::: α emitters :::
        "Am-241": {"Z": 95, "A": 241},
        "Ra-224": {"Z": 88, "A": 224},
        "Pu-239": {"Z": 94, "A": 239},
        "Ra-226": {"Z": 88, "A": 226},
        "Ac-225": {"Z": 89, "A": 225},
        "Th-232": {"Z": 90, "A": 232},
        "Th-228": {"Z": 90, "A": 228},
        "U-238":  {"Z": 92, "A": 238},
        "U-235":  {"Z": 92, "A": 235},
        "At-211": {"Z": 85, "A": 211},
        "Po-210": {"Z": 84, "A": 210},
        "Cm-244": {"Z": 96, "A": 244},
        "Cf-252": {"Z": 98, "A": 252},
        "Rn-222": {"Z": 86, "A": 222},

        # ::: β- emitters :::
        "Sr-90":  {"Z": 38, "A": 90},
        "Y-90":   {"Z": 39, "A": 90},
        "P-32":   {"Z": 15, "A": 32},
        "S-35":   {"Z": 16, "A": 35},
        "Lu-177": {"Z": 71, "A": 177},
        "Re-188": {"Z": 75, "A": 188},
        "Re-186": {"Z": 75, "A": 186},
        "Sm-153": {"Z": 62, "A": 153},
        "Ho-166": {"Z": 67, "A": 166},
        "I-131":  {"Z": 53, "A": 131},
        "Ir-192": {"Z": 77, "A": 192},
        "Fe-59":  {"Z": 26, "A": 59},
        "Cs-137": {"Z": 55, "A": 137},  # β- → Ba-137m (γ 662 keV)
        "Co-60":  {"Z": 27, "A": 60},   # β- + γ (1.17, 1.33 MeV)
        "Na-24":  {"Z": 11, "A": 24},   

        # ::: Beta+ emitters :::
        "F-18":  {"Z": 9,  "A": 18},
        "C-11":  {"Z": 6,  "A": 11},
        "N-13":  {"Z": 7,  "A": 13},
        "O-15":  {"Z": 8,  "A": 15},
        "Ga-68": {"Z": 31, "A": 68},
        "Zr-89": {"Z": 40, "A": 89},
        "Cu-64": {"Z": 29, "A": 64},  # β+ and β-
        "Sc-44": {"Z": 21, "A": 44},
        "Rb-82": {"Z": 37, "A": 82},
        "Na-22": {"Z": 11, "A": 22},
        "I-124": {"Z": 53, "A": 124},
        "Y-86":  {"Z": 39, "A": 86},
        "Br-76": {"Z": 35, "A": 76},

        # ::: Gamma emitters :::
        "Tc-99m": {"Z": 43, "A": 99},
        "Co-57":  {"Z": 27, "A": 57},
        "Co-60":  {"Z": 27, "A": 60},
        "Cs-137": {"Z": 55, "A": 137},
        "Ba-133": {"Z": 56, "A": 133},
        "Na-22":  {"Z": 11, "A": 22},
        "Am-241": {"Z": 95, "A": 241},  # 59.5 keV γ
        "Mn-54":  {"Z": 25, "A": 54},
        "Zn-65":  {"Z": 30, "A": 65},
        "Fe-59":  {"Z": 26, "A": 59},
        "Cd-109": {"Z": 48, "A": 109},
        "In-111": {"Z": 49, "A": 111},
        "Tl-201": {"Z": 81, "A": 201},
        "Xe-133": {"Z": 54, "A": 133},
        "Kr-85":  {"Z": 36, "A": 85},
        "I-125":  {"Z": 53, "A": 125},
}


# :::::: Command-based Scoring for Square detector ::::::
    if detector_choice == "Box":
        CommandBasedScoring = f"""# ::::::::::::::::::::::::::::::::::::::::::::
# :::         Command-Based Scoring        :::
# ::::::::::::::::::::::::::::::::::::::::::::

/score/create/boxMesh             DetScoringVolume   # Name of scoring mesh
/score/mesh/boxSize               {DetX:.2f} {DetY:.2f} {DetZ:.2f} mm
/score/mesh/nBin                  {voxX:.0f} {voxY:.0f} {voxZ:.0f}
/score/mesh/translate/xyz         {detector_pos_values[0]} {detector_pos_values[1]} {detector_pos_values[2]} mm

/score/quantity/energyDeposit      EnergyDep MeV      # Quantity to score
/score/filter/particle gammaFilter gamma              # Particle Filter
/score/close                                          # Closing the mesh """  

        CommandBasedScoringVisualization = f"""# ::::::::::::::::::::::::::::::::::::::::::
# ::: Command-Based Scorer Visualization :::
# ::::::::::::::::::::::::::::::::::::::::::

# Uncomment the following lines ONLY IF you want to verify the scorer geometry using interactive mode
# Terminal% ./run.sh --vis
# Session: /control/execute MC-ADD.mac

#/vis/drawVolume worlds
#/vis/viewer/copyViewFrom viewer-0
#/score/colorMap/setMinMax ! 0. 800.
#/control/loop drawSlice.mac iColumn 0 0 1 # Second number is the number of slices depending on the no of bins defined previously


# :::::::::::::::::::::::::::::::::::::::::::
# :::            Scoring Files            :::
# :::::::::::::::::::::::::::::::::::::::::::

# To save more scored quantities use: /score/dumpQuantityToFile ScoringMeshName QuantityToScore FileName.csv 

/score/dumpQuantityToFile DetScoringVolume EnergyDep GammaEnergyDep.csv 
"""
    elif detector_choice == "Cylinder":
        CommandBasedScoring = f"""# ::::::::::::::::::::::::::::::::::::::::::::
# :::         Command-Based Scoring        :::
# ::::::::::::::::::::::::::::::::::::::::::::

/score/create/cylinderMesh        DetScoringVolume   # Name of scoring mesh
/score/mesh/cylinderSize          {detector_dim_values[1]} {DetLen:.2f} mm
/score/mesh/nBin                  {iR:.0f} {iZ:.0f} {iPhi:.0f}               # R Z Phi
/score/mesh/translate/xyz         {detector_pos_values[0]} {detector_pos_values[1]} {detector_pos_values[2]} mm
/score/mesh/rotate/rotateX        90 deg

/score/quantity/energyDeposit      EnergyDep MeV      # Quantity to score
/score/filter/particle gammaFilter gamma              # Particle Filter
/score/close                                          # Closing the mesh """

        CommandBasedScoringVisualization =f"""# ::::::::::::::::::::::::::::::::::::::::::
# ::: Command-Based Scorer Visualization :::
# ::::::::::::::::::::::::::::::::::::::::::

# Uncomment the following lines ONLY IF you want to verify the scorer geometry using interactive mode
# Terminal% ./run.sh --vis
# Session: /control/execute MC-ADD.mac

#/score/colorMap/setMinMax ! 0. 200.
#/control/alias iAxis 1
#/control/loop drawCylinderSlice.mac iColumn 0 {cylinderVis:.0f} 1


# :::::::::::::::::::::::::::::::::::::::::::
# :::            Scoring Files            :::
# :::::::::::::::::::::::::::::::::::::::::::

# To save more scored quantities use: /score/dumpQuantityToFile ScoringMeshName QuantityToScore FileName.csv 

/score/dumpQuantityToFile DetScoringVolume EnergyDep CylinderGammaEnergyDep.csv 
"""
    

# :::::: Macro File Template ::::::
    if Radionuclide in radionuclides:               # Check if radionuclide is supported
            Z = radionuclides[Radionuclide]["Z"]
            A = radionuclides[Radionuclide]["A"]
            
            if source_choice == "Cylinder": 
                # ::: Cylindrical source :::
                MacroFileTemplate = f"""# ::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::
# :::                            :::
# :::   MC-ADD macrofile    :::
# :::                            :::
# ::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::

#/run/numberOfThreads 16   # If you enabled multithreaded mode

/run/initialize 
/control/verbose   0
/run/verbose       0
/tracking/verbose  0


{CommandBasedScoring}


# ::::::::::::::::::::::::::::::::::::::::::::
# :::         Enable Radioactive Decay     :::
# ::::::::::::::::::::::::::::::::::::::::::::

# This command line is needed so that Geant4 enables the radioactive decay of long-lived ions
/process/had/rdm/thresholdForVeryLongDecayTime 1.0e+60 y


# ::::::::::::::::::::::::::::::::::::::::::::
# :::         Sources properties           :::
# :::                 &                    :::
# :::   Source position and structure      :::
# ::::::::::::::::::::::::::::::::::::::::::::

# Commands used in this macrofile:
#/gps/particle       name        || We define the particle type. In this case, it will be gamma
#/gps/ion            Z A Q E     || We define the gamma based on it Z and A. Q: charge. E: energy
#/gps/energy         E keV       || We set the particle energy
#/gps/pos/type       dist        || We set the type of distribution
#/gps/ang/type       AgDis       || We define the angular distribution. Isotropic emission (iso) is selected by default
#/gps/pos/shape      Cylinder    || We define the shape of the source
#/gps/pos/radius     X mm        || We define the radius of the source
#/gps/pos/halfz      X mm        || We define the half-lenght of the source
#/gps/pos/centre     X X X mm    || We define the position of the source
#/gps/pos/confine    source      || We confine the source in the physical volume
#/gps/pos/rot1                   || We define a rotation. Default [1, 0, 0]
#/gps/pos/rot2                   || We define a second rotation. Default [0, 1, 0] 

# ::: {Radionuclide} :::
/gps/particle             ion
/gps/ion                  {Z} {A} 0 0
/gps/ang/type             iso
/gps/pos/type             {Location_source}
/gps/pos/shape            {source_choice}
/gps/pos/radius           {source_dim_values[1]} mm
/gps/pos/halfz            {halfz:.2f} mm
/gps/pos/rot1             1 0 0
/gps/pos/rot2             0 0 1 
/gps/energy               0 keV
/gps/pos/centre           {source_pos_values[0]} {source_pos_values[1]} {source_pos_values[2]} mm


# :::::::::::::::::::::::::::::::::::::::::::
# :::            Run Beam On              :::
# :::::::::::::::::::::::::::::::::::::::::::

/run/beamOn               {Runs_input} 


{CommandBasedScoringVisualization}
"""

            elif source_choice == "Box":
                # ::: Square source :::
                MacroFileTemplate = f"""# ::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::
# :::                            :::
# :::   MC-ADD macrofile    :::
# :::                            :::
# ::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::

#/run/numberOfThreads 16   # If you enabled multithreaded mode

/run/initialize 
/control/verbose   0
/run/verbose       0
/tracking/verbose  0


{CommandBasedScoring}


# ::::::::::::::::::::::::::::::::::::::::::::
# :::         Enable Radioactive Decay     :::
# ::::::::::::::::::::::::::::::::::::::::::::

# This command line is needed so that Geant4 enables the radioactive decay of long-lived ions
/process/had/rdm/thresholdForVeryLongDecayTime 1.0e+60 y


# ::::::::::::::::::::::::::::::::::::::::::::
# :::         Sources properties           :::
# :::                 &                    :::
# :::   Source position and structure      :::
# ::::::::::::::::::::::::::::::::::::::::::::

# Commands used in this macrofile:
#/gps/particle       name        || We define the particle type. In this case, it will be gamma
#/gps/ion            Z A Q E     || We define the gamma based on it Z and A. Q: charge. E: energy
#/gps/energy         E keV       || We set the particle energy
#/gps/pos/type       dist        || We set the type of distribution
#/gps/ang/type       AgDis       || We define the angular distribution. Isotropic emission (iso) is selected by default
#/gps/pos/shape      Cylinder    || We define the shape of the source
#/gps/pos/radius     X mm        || We define the radius of the source
#/gps/pos/halfz      X mm        || We define the half-lenght of the source
#/gps/pos/centre     X X X mm    || We define the position of the source
#/gps/pos/confine    source      || We confine the source in the physical volume
#/gps/pos/rot1                   || We define a rotation. Default [1, 0, 0]
#/gps/pos/rot2                   || We define a second rotation. Default [0, 1, 0] 

# ::: {Radionuclide} :::
/gps/particle             ion
/gps/ion                  {Z} {A} 0 0
/gps/ang/type             iso
/gps/pos/type             {Location_source}
/gps/pos/shape            Para
/gps/pos/halfx            {halfx:.2f} mm
/gps/pos/halfy            {halfy:.2f} mm
/gps/pos/halfz            {halfz:.2f} mm
/gps/pos/rot1             1 0 0
/gps/pos/rot2             0 0 1 
/gps/energy               0 keV
/gps/pos/centre           {source_pos_values[0]} {source_pos_values[1]} {source_pos_values[2]} mm


# :::::::::::::::::::::::::::::::::::::::::::
# :::            Run Beam On              :::
# :::::::::::::::::::::::::::::::::::::::::::

/run/beamOn               {Runs_input} 


{CommandBasedScoringVisualization}
"""
            else:
                print("Error: Unsupported source shape choice.")
                exit(1)  # Ensure the script stops if an unsupported source is selected
                

# :::::: Generating the Macro File ::::::
            with open("MC-ADD.mac", "w") as macrofile:
                macrofile.write(MacroFileTemplate)
        
    else:
        print("Error: Unsupported radionuclide.")

    messagebox.showinfo("Success!", "Your DetectorConstruction.cc and macro file have been generated!")


    shutil.copy(SourceCCFile, DestinationCCFile)                                  # Copy the file to the destination 
    os.replace(SourceCCFile, DestinationCCFile)
    shutil.move(geometryName +".txt", DestinationTxtFile)                         # Moving DetectorConstruction.txt into DetectorConstructionGeometries folder


# Function to close the GUI window
def close_window():
    root.destroy()


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::                                                                                                                                                                          :::::::::
# :::::::::                                                                       G U I                                                                                              :::::::::
# :::::::::                                                                                                                                                                          :::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

root = tk.Tk()
root.title("MC-ADD")      # Title
root.geometry("1000x600")      # Window size
root.configure(bg="#F5F5F5")   # background color (white)


# ::::::::::::::::::::::::: BLUE STRIPES :::::::::::::::::::::::::

# ::: Color :::
blue_color  = "#0033a1"

# ::: Top :::
top_stripe = tk.Frame(root, bg=blue_color, height=30)
top_stripe.pack(fill=tk.X)

# ::: Bottom :::
bottom_stripe = tk.Frame(root, bg=blue_color, height=30)
bottom_stripe.pack(side=tk.BOTTOM, fill=tk.X)

# ::: Separation line :::
separation_line = tk.Frame(root, bg=blue_color, height=2)
separation_line.place(x=0, y=400, width=1000)



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                       G U I    T I T L E                       :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

title = tk.Label(root, text="MC-ADD", font=("Times New Roman", 20, "bold"), fg=blue_color, bg="#F5F5F5")
title.place(x=500, y=45, anchor=tk.CENTER)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                          W O R L D                             :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# :::::: TITLE ::::::
world_label = tk.Label(root, text="World", font=("Times New Roman", 15), bg="#F5F5F5", fg="black", width=23, anchor="center", justify="center")
world_label.place(x=120, y=75)

# :::::: SHPAPE ::::::
world_shape = tk.Label(root, text="Box", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
world_shape.place(x=122, y=120)

# :::::: DIMENSIONS ::::::
world_dims = tk.Label(root, text="Fixed to 2x2x2 m", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
world_dims.place(x=122, y=180)

# :::::: POSITION ::::::
Fixed_pos = tk.Label(root, text="Fixed to 0 0 0", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
Fixed_pos.place(x=122,y=270)

# :::::: MATERIALS ::::::
world_material_combobox = ttk.Combobox(root, values=["G4_AIR", "G4_WATER"], state="readonly", font=("Times New Roman", 12), width = 27)
world_material_combobox.place(x=121, y=340)     
world_material_combobox.set("Select Material")  


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                       S O U R C E                              :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# :::::: TITLE ::::::
source_label = tk.Label(root, text="Source", font=("Times New Roman", 15), bg="#F5F5F5", fg="black", width=23, anchor="center", justify="center")
source_label.place(x=320, y=75)

# :::::: SHAPE ::::::
source_combobox = ttk.Combobox(root, values=["Box", "Cylinder"], state="readonly", font=("Times New Roman", 12), width = 27)
source_combobox.place(x=321, y=120)
source_combobox.set("Choose Shape")

# :::::: DIMENSIONS ::::::
source_dim1 = tk.Entry(root, width=5)
source_dim1.place(x=321, y=180)
source_dim2 = tk.Entry(root, width=5)
source_dim2.place(x=387.5, y=180)
source_dim3 = tk.Entry(root, width=5)
source_dim3.place(x=454, y=180) 


# ::: DIMENSIONS LABELS :::
# ::: Box :::
SourceDimSq_label = tk.Label(root, text="x                    y                    z", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
SourceDimSq_label.place(x=322, y=210)

# ::: Cylinder :::
SourceDimCyl_label = tk.Label(root, text="radius 1         radius 2        thickness", font=("Times New Roman", 12), bg="#F5F5F5", fg="black")
SourceDimCyl_label.place(x=329, y=233)

# :::::: POSITION ::::::
source_pos1 = tk.Entry(root, width=5)
source_pos1.place(x=321, y=270)
source_pos2 = tk.Entry(root, width=5)
source_pos2.place(x=387.5, y=270)
source_pos3 = tk.Entry(root, width=5)
source_pos3.place(x=454, y=270)

DetectorPos_label = tk.Label(root, text="x                    y                    z", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
DetectorPos_label.place(x=322, y=300)

# :::::: MATERIALS ::::::
source_material_combobox = ttk.Combobox(root, values=["G4_H", "G4_He", "G4_Li", "G4_Be", "G4_B", "G4_C", "G4_N", "G4_O", 
"G4_F", "G4_Ne", "G4_Na", "G4_Mg", "G4_Al", "G4_Si", "G4_P", "G4_S", "G4_Cl", "G4_Ar", "G4_K", "G4_Ca", "G4_Sc", "G4_Ti", "G4_V", "G4_Cr", 
"G4_Mn", "G4_Fe", "G4_Co", "G4_Ni", "G4_Cu", "G4_Zn", "G4_Ga", "G4_Ge", "G4_As", "G4_Se", "G4_Br", "G4_Kr", "G4_Rb", "G4_Sr", "G4_Y", "G4_Zr",
"G4_Nb", "G4_Mo", "G4_Tc", "G4_Ru", "G4_Rh", "G4_Pd", "G4_Ag", "G4_Cd", "G4_In", "G4_Sn", "G4_Sb", "G4_Te", "G4_I", "G4_Xe", "G4_Cs", "G4_Ba", 
"G4_La", "G4_Ce", "G4_Pr", "G4_Nd", "G4_Pm", "G4_Sm", "G4_Eu", "G4_Gd", "G4_Tb", "G4_Dy", "G4_Ho", "G4_Er", "G4_Tm", "G4_Yb", "G4_Lu", "G4_Hf", 
"G4_Ta", "G4_W", "G4_Re", "G4_Os", "G4_Ir", "G4_Pt", "G4_Au", "G4_Hg", "G4_Tl", "G4_Pb", "G4_Bi", "G4_Po", "G4_At", "G4_Rn", "G4_Fr", "G4_Ra", 
"G4_Ac", "G4_Th", "G4_Pa", "G4_U", "G4_Np", "G4_Pu", "G4_Am", "G4_Cm", "G4_Bk", "G4_Cf", "G4_A-150_TISSUE", "G4_ACETONE", "G4_ACETYLENE", 
"G4_ADENINE", "G4_ADIPOSE_TISSUE_ICRP", "G4_AIR", "G4_ALANINE", "G4_ALUMINUM_OXIDE", "G4_AMBER", "G4_AMMONIA", "G4_ANILINE", "G4_ANTHRACENE", 
"G4_B-100_BONE", "G4_BAKELITE", "G4_BARIUM_FLUORIDE", "G4_BARIUM_SULFATE", "G4_BENZENE", "G4_BERYLLIUM_OXIDE", "G4_BGO", "G4_BLOOD_ICRP", 
"G4_BONE_COMPACT_ICRU", "G4_BONE_CORTICAL_ICRP", "G4_BORON_CARBIDE", "G4_BORON_OXIDE", "G4_BRAIN_ICRP", "G4_BUTANE", "G4_N-BUTYL_ALCOHOL", 
"G4_C-552", "G4_CADMIUM_TELLURIDE", "G4_CADMIUM_TUNGSTATE", "G4_CALCIUM_CARBONATE", "G4_CALCIUM_FLUORIDE", "G4_CALCIUM_OXIDE", "G4_CALCIUM_SULFATE",
"G4_CALCIUM_TUNGSTATE", "G4_CARBON_DIOXIDE", "G4_CARBON_TETRACHLORIDE", "G4_CELLULOSE_CELLOPHANE", "G4_CELLULOSE_BUTYRATE", "G4_CELLULOSE_NITRATE", 
"G4_CERIC_SULFATE", "G4_CESIUM_FLUORIDE", "G4_CESIUM_IODIDE", "G4_CHLOROBENZENE", "G4_CHLOROFORM", "G4_CONCRETE", "G4_CYCLOHEXANE", "G4_1,2-DICHLOROBENZENE", 
"G4_DICHLORODIETHYL_ETHER", "G4_1,2-DICHLOROETHANE", "G4_DIETHYL_ETHER", "G4_N,N-DIMETHYL_FORMAMIDE", "G4_DIMETHYL_SULFOXIDE", "G4_ETHANE", "G4_ETHYL_ALCOHOL",
"G4_ETHYL_CELLULOSE", "G4_ETHYLENE", "G4_EYE_LENS_ICRP", "G4_FERRIC_OXIDE", "G4_FERROBORIDE", "G4_FERROUS_OXIDE", "G4_FERROUS_SULFATE", "G4_FREON-12", 
"G4_FREON-12B2", "G4_FREON-13", "G4_FREON-13B1", "G4_FREON-13I1", "G4_GADOLINIUM_OXYSULFIDE", "G4_GALLIUM_ARSENIDE", "G4_GEL_PHOTO_EMULSION", "G4_Pyrex_Glass",
"G4_GLASS_LEAD", "G4_GLASS_PLATE", "G4_GLUTAMINE", "G4_GLYCEROL", "G4_GUANINE", "G4_GYPSUM", "G4_KAPTON", "G4_LANTHANUM_OXYBROMIDE", "G4_LANTHANUM_OXYSULFIDE", 
"G4_LEAD_OXIDE", "G4_LITHIUM_AMIDE", "G4_LITHIUM_CARBONATE", "G4_LITHIUM_FLUORIDE", "G4_LITHIUM_HYDRIDE", "G4_LITHIUM_IODIDE", "G4_LITHIUM_OXIDE",
"G4_LITHIUM_TETRABORATE", "G4_LUNG_ICRP", "G4_M3_WAX", "G4_MAGNESIUM_CARBONATE", "G4_MAGNESIUM_FLUORIDE", "G4_MAGNESIUM_OXIDE", "G4_MAGNESIUM_TETRABORATE", 
"G4_MERCURIC_IODIDE", "G4_METHANE", "G4_METHANOL", "G4_MIX_D_WAX", "G4_MS20_TISSUE", "G4_MUSCLE_SKELETAL_ICRP", "G4_MUSCLE_STRIATED_ICRU", "G4_MUSCLE_WITH_SUCROSE",
"G4_MUSCLE_WITHOUT_SUCROSE", "G4_NAPHTHALENE", "G4_NITROBENZENE", "G4_NITROUS_OXIDE", "G4_NYLON-8062", "G4_NYLON-6-6", "G4_NYLON-6-10", "G4_NYLON-11_RILSAN",
"G4_OCTANE", "G4_PARAFFIN", "G4_N-PENTANE", "G4_PHOTO_EMULSION", "G4_PLASTIC_SC_VINYLTOLUENE", "G4_PLUTONIUM_DIOXIDE", "G4_POLYACRYLONITRILE", "G4_POLYCARBONATE",
"G4_POLYCHLOROSTYRENE", "G4_POLYETHYLENE", "G4_MYLAR", "G4_PLEXIGLASS", "G4_POLYOXYMETHYLENE", "G4_POLYPROPYLENE", "G4_POLYSTYRENE", "G4_TEFLON", 
"G4_POLYTRIFLUOROCHLOROETHYLENE", "G4_POLYVINYL_ACETATE", "G4_POLYVINYL_ALCOHOL", "G4_POLYVINYL_BUTYRAL", "G4_POLYVINYL_CHLORIDE", "G4_POLYVINYLIDENE_CHLORIDE",
"G4_POLYVINYLIDENE_FLUORIDE", "G4_POLYVINYL_PYRROLIDONE", "G4_POTASSIUM_IODIDE", "G4_POTASSIUM_OXIDE", "G4_PROPANE", "G4_lPROPANE", "G4_N-PROPYL_ALCOHOL",
"G4_PYRIDINE", "G4_RUBBER_BUTYL", "G4_RUBBER_NATURAL", "G4_RUBBER_NEOPRENE", "G4_SILICON_DIOXIDE", "G4_SILVER_BROMIDE", "G4_SILVER_CHLORIDE", "G4_SILVER_HALIDES",
"G4_SILVER_IODIDE", "G4_SKIN_ICRP", "G4_SODIUM_CARBONATE", "G4_SODIUM_IODIDE", "G4_SODIUM_MONOXIDE", "G4_SODIUM_NITRATE", "G4_STILBENE", "G4_SUCROSE", "G4_TERPHENYL",
"G4_TESTIS_ICRP", "G4_TETRACHLOROETHYLENE", "G4_THALLIUM_CHLORIDE", "G4_TISSUE_SOFT_ICRP", "G4_TISSUE_SOFT_ICRU-4", "G4_TISSUE-METHANE", "G4_TISSUE-PROPANE",
"G4_TITANIUM_DIOXIDE", "G4_TOLUENE", "G4_TRICHLOROETHYLENE", "G4_TRIETHYL_PHOSPHATE", "G4_TUNGSTEN_HEXAFLUORIDE", "G4_URANIUM_DICARBIDE", "G4_URANIUM_MONOCARBIDE", 
"G4_URANIUM_OXIDE", "G4_UREA", "G4_VALINE", "G4_VITON", "G4_WATER", "G4_WATER_VAPOR", "G4_XYLENE", "G4_GRAPHITE", "G4_lH2", "G4_lN2", "G4_lO2", "G4_lAr", "G4_lBr", 
"G4_lKr", "G4_lXe", "G4_PbWO4", "G4_Galactic", "G4_GRAPHITE_POROUS", "G4_LUCITE", "G4_BRASS", "G4_BRONZE", "G4_STAINLESS-STEEL", "G4_CR39", "G4_OCTADECANOL",
"G4_KEVLAR", "G4_DACRON", "G4_NEOPRENE", "G4_CYTOSINE", "G4_THYMINE", "G4_URACIL", "G4_DNA_ADENINE", "G4_DNA_GUANINE", "G4_DNA_CYTOSINE", "G4_DNA_THYMINE", 
"G4_DNA_URACIL", "G4_DNA_ADENOSINE", "G4_DNA_GUANOSINE", "G4_DNA_CYTIDINE", "G4_DNA_URIDINE", "G4_DNA_METHYLURIDINE", "G4_DNA_MONOPHOSPHATE", "G4_DNA_A", 
"G4_DNA_G", "G4_DNA_C", "G4_DNA_U", "G4_DNA_MU"], state="readonly", font=("Times New Roman", 12), width=27)
source_material_combobox.place(x=321, y=340)
source_material_combobox.set("Select Material")


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                       D E T E C T O R                          :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# :::::: TITLE ::::::
detector_label = tk.Label(root, text="Detector", font=("Times New Roman", 15), bg="#F5F5F5", fg="black", width=23, anchor="center", justify="center")
detector_label.place(x=525, y=75)


# :::::: SHAPE ::::::
detector_combobox = ttk.Combobox(root, values=["Box", "Cylinder"], state="readonly", font=("Times New Roman", 12), width = 27)
detector_combobox.place(x=526, y=120)
detector_combobox.set("Choose Shape")

# :::::: DIMENSIONS ::::::
detector_dim1 = tk.Entry(root, width=5)
detector_dim1.place(x=527, y=180)
detector_dim2 = tk.Entry(root, width=5)
detector_dim2.place(x=592.2, y=180)
detector_dim3 = tk.Entry(root, width=5)
detector_dim3.place(x=656, y=180)

# ::: DIMENSIONS LABELS :::
# ::: Box :::
DetectorDimSq_label = tk.Label(root, text="x                    y                    z", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
DetectorDimSq_label.place(x=527, y=210)

# ::: Cylinder :::
DetectorDimCyl_label = tk.Label(root, text="radius 1         radius 2        thickness", font=("Times New Roman", 12), bg="#F5F5F5", fg="black")
DetectorDimCyl_label.place(x=534, y=233)


# :::::: POSITIONS ::::::
detector_pos1 = tk.Entry(root, width=5)
detector_pos1.place(x=527, y=270)
detector_pos2 = tk.Entry(root, width=5)
detector_pos2.place(x=592.2, y=270)
detector_pos3 = tk.Entry(root, width=5)
detector_pos3.place(x=656, y=270) 

DetectorPos_label = tk.Label(root, text="x                    y                    z", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
DetectorPos_label.place(x=527, y=300) 


# :::::: MATERIALS ::::::
detector_material_combobox = ttk.Combobox(root, values=["G4_H", "G4_He", "G4_Li", "G4_Be", "G4_B", "G4_C", "G4_N", "G4_O", 
"G4_F", "G4_Ne", "G4_Na", "G4_Mg", "G4_Al", "G4_Si", "G4_P", "G4_S", "G4_Cl", "G4_Ar", "G4_K", "G4_Ca", "G4_Sc", "G4_Ti", "G4_V", "G4_Cr", 
"G4_Mn", "G4_Fe", "G4_Co", "G4_Ni", "G4_Cu", "G4_Zn", "G4_Ga", "G4_Ge", "G4_As", "G4_Se", "G4_Br", "G4_Kr", "G4_Rb", "G4_Sr", "G4_Y", "G4_Zr",
"G4_Nb", "G4_Mo", "G4_Tc", "G4_Ru", "G4_Rh", "G4_Pd", "G4_Ag", "G4_Cd", "G4_In", "G4_Sn", "G4_Sb", "G4_Te", "G4_I", "G4_Xe", "G4_Cs", "G4_Ba", 
"G4_La", "G4_Ce", "G4_Pr", "G4_Nd", "G4_Pm", "G4_Sm", "G4_Eu", "G4_Gd", "G4_Tb", "G4_Dy", "G4_Ho", "G4_Er", "G4_Tm", "G4_Yb", "G4_Lu", "G4_Hf", 
"G4_Ta", "G4_W", "G4_Re", "G4_Os", "G4_Ir", "G4_Pt", "G4_Au", "G4_Hg", "G4_Tl", "G4_Pb", "G4_Bi", "G4_Po", "G4_At", "G4_Rn", "G4_Fr", "G4_Ra", 
"G4_Ac", "G4_Th", "G4_Pa", "G4_U", "G4_Np", "G4_Pu", "G4_Am", "G4_Cm", "G4_Bk", "G4_Cf", "G4_A-150_TISSUE", "G4_ACETONE", "G4_ACETYLENE", 
"G4_ADENINE", "G4_ADIPOSE_TISSUE_ICRP", "G4_AIR", "G4_ALANINE", "G4_ALUMINUM_OXIDE", "G4_AMBER", "G4_AMMONIA", "G4_ANILINE", "G4_ANTHRACENE", 
"G4_B-100_BONE", "G4_BAKELITE", "G4_BARIUM_FLUORIDE", "G4_BARIUM_SULFATE", "G4_BENZENE", "G4_BERYLLIUM_OXIDE", "G4_BGO", "G4_BLOOD_ICRP", 
"G4_BONE_COMPACT_ICRU", "G4_BONE_CORTICAL_ICRP", "G4_BORON_CARBIDE", "G4_BORON_OXIDE", "G4_BRAIN_ICRP", "G4_BUTANE", "G4_N-BUTYL_ALCOHOL", 
"G4_C-552", "G4_CADMIUM_TELLURIDE", "G4_CADMIUM_TUNGSTATE", "G4_CALCIUM_CARBONATE", "G4_CALCIUM_FLUORIDE", "G4_CALCIUM_OXIDE", "G4_CALCIUM_SULFATE",
"G4_CALCIUM_TUNGSTATE", "G4_CARBON_DIOXIDE", "G4_CARBON_TETRACHLORIDE", "G4_CELLULOSE_CELLOPHANE", "G4_CELLULOSE_BUTYRATE", "G4_CELLULOSE_NITRATE", 
"G4_CERIC_SULFATE", "G4_CESIUM_FLUORIDE", "G4_CESIUM_IODIDE", "G4_CHLOROBENZENE", "G4_CHLOROFORM", "G4_CONCRETE", "G4_CYCLOHEXANE", "G4_1,2-DICHLOROBENZENE", 
"G4_DICHLORODIETHYL_ETHER", "G4_1,2-DICHLOROETHANE", "G4_DIETHYL_ETHER", "G4_N,N-DIMETHYL_FORMAMIDE", "G4_DIMETHYL_SULFOXIDE", "G4_ETHANE", "G4_ETHYL_ALCOHOL",
"G4_ETHYL_CELLULOSE", "G4_ETHYLENE", "G4_EYE_LENS_ICRP", "G4_FERRIC_OXIDE", "G4_FERROBORIDE", "G4_FERROUS_OXIDE", "G4_FERROUS_SULFATE", "G4_FREON-12", 
"G4_FREON-12B2", "G4_FREON-13", "G4_FREON-13B1", "G4_FREON-13I1", "G4_GADOLINIUM_OXYSULFIDE", "G4_GALLIUM_ARSENIDE", "G4_GEL_PHOTO_EMULSION", "G4_Pyrex_Glass",
"G4_GLASS_LEAD", "G4_GLASS_PLATE", "G4_GLUTAMINE", "G4_GLYCEROL", "G4_GUANINE", "G4_GYPSUM", "G4_KAPTON", "G4_LANTHANUM_OXYBROMIDE", "G4_LANTHANUM_OXYSULFIDE", 
"G4_LEAD_OXIDE", "G4_LITHIUM_AMIDE", "G4_LITHIUM_CARBONATE", "G4_LITHIUM_FLUORIDE", "G4_LITHIUM_HYDRIDE", "G4_LITHIUM_IODIDE", "G4_LITHIUM_OXIDE",
"G4_LITHIUM_TETRABORATE", "G4_LUNG_ICRP", "G4_M3_WAX", "G4_MAGNESIUM_CARBONATE", "G4_MAGNESIUM_FLUORIDE", "G4_MAGNESIUM_OXIDE", "G4_MAGNESIUM_TETRABORATE", 
"G4_MERCURIC_IODIDE", "G4_METHANE", "G4_METHANOL", "G4_MIX_D_WAX", "G4_MS20_TISSUE", "G4_MUSCLE_SKELETAL_ICRP", "G4_MUSCLE_STRIATED_ICRU", "G4_MUSCLE_WITH_SUCROSE",
"G4_MUSCLE_WITHOUT_SUCROSE", "G4_NAPHTHALENE", "G4_NITROBENZENE", "G4_NITROUS_OXIDE", "G4_NYLON-8062", "G4_NYLON-6-6", "G4_NYLON-6-10", "G4_NYLON-11_RILSAN",
"G4_OCTANE", "G4_PARAFFIN", "G4_N-PENTANE", "G4_PHOTO_EMULSION", "G4_PLASTIC_SC_VINYLTOLUENE", "G4_PLUTONIUM_DIOXIDE", "G4_POLYACRYLONITRILE", "G4_POLYCARBONATE",
"G4_POLYCHLOROSTYRENE", "G4_POLYETHYLENE", "G4_MYLAR", "G4_PLEXIGLASS", "G4_POLYOXYMETHYLENE", "G4_POLYPROPYLENE", "G4_POLYSTYRENE", "G4_TEFLON", 
"G4_POLYTRIFLUOROCHLOROETHYLENE", "G4_POLYVINYL_ACETATE", "G4_POLYVINYL_ALCOHOL", "G4_POLYVINYL_BUTYRAL", "G4_POLYVINYL_CHLORIDE", "G4_POLYVINYLIDENE_CHLORIDE",
"G4_POLYVINYLIDENE_FLUORIDE", "G4_POLYVINYL_PYRROLIDONE", "G4_POTASSIUM_IODIDE", "G4_POTASSIUM_OXIDE", "G4_PROPANE", "G4_lPROPANE", "G4_N-PROPYL_ALCOHOL",
"G4_PYRIDINE", "G4_RUBBER_BUTYL", "G4_RUBBER_NATURAL", "G4_RUBBER_NEOPRENE", "G4_SILICON_DIOXIDE", "G4_SILVER_BROMIDE", "G4_SILVER_CHLORIDE", "G4_SILVER_HALIDES",
"G4_SILVER_IODIDE", "G4_SKIN_ICRP", "G4_SODIUM_CARBONATE", "G4_SODIUM_IODIDE", "G4_SODIUM_MONOXIDE", "G4_SODIUM_NITRATE", "G4_STILBENE", "G4_SUCROSE", "G4_TERPHENYL",
"G4_TESTIS_ICRP", "G4_TETRACHLOROETHYLENE", "G4_THALLIUM_CHLORIDE", "G4_TISSUE_SOFT_ICRP", "G4_TISSUE_SOFT_ICRU-4", "G4_TISSUE-METHANE", "G4_TISSUE-PROPANE",
"G4_TITANIUM_DIOXIDE", "G4_TOLUENE", "G4_TRICHLOROETHYLENE", "G4_TRIETHYL_PHOSPHATE", "G4_TUNGSTEN_HEXAFLUORIDE", "G4_URANIUM_DICARBIDE", "G4_URANIUM_MONOCARBIDE", 
"G4_URANIUM_OXIDE", "G4_UREA", "G4_VALINE", "G4_VITON", "G4_WATER", "G4_WATER_VAPOR", "G4_XYLENE", "G4_GRAPHITE", "G4_lH2", "G4_lN2", "G4_lO2", "G4_lAr", "G4_lBr", 
"G4_lKr", "G4_lXe", "G4_PbWO4", "G4_Galactic", "G4_GRAPHITE_POROUS", "G4_LUCITE", "G4_BRASS", "G4_BRONZE", "G4_STAINLESS-STEEL", "G4_CR39", "G4_OCTADECANOL",
"G4_KEVLAR", "G4_DACRON", "G4_NEOPRENE", "G4_CYTOSINE", "G4_THYMINE", "G4_URACIL", "G4_DNA_ADENINE", "G4_DNA_GUANINE", "G4_DNA_CYTOSINE", "G4_DNA_THYMINE", 
"G4_DNA_URACIL", "G4_DNA_ADENOSINE", "G4_DNA_GUANOSINE", "G4_DNA_CYTIDINE", "G4_DNA_URIDINE", "G4_DNA_METHYLURIDINE", "G4_DNA_MONOPHOSPHATE", "G4_DNA_A", 
"G4_DNA_G", "G4_DNA_C", "G4_DNA_U", "G4_DNA_MU"], state="readonly", font=("Times New Roman", 12), width = 27)
detector_material_combobox.place(x=526, y=340)
detector_material_combobox.set("Select Material")


# ::: DIMENSIONS* CLARIFICATION :::
note_label = tk.Label(root, text="* Dimensions should be given in mm", font=("Times New Roman", 10), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
note_label.place(x=425, y=370) 


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                   C A D    G E O M E T R I E S                 :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# ::: TITLE :::
cad_label = tk.Label(root, text="Mesh Geometries", font=("Times New Roman", 15), bg="#F5F5F5", fg="black", width=23, anchor="center", justify="center")
cad_label.place(x=751, y=75)


# ::: INPUT FIELD :::
CAD_Input = tk.Entry(root, width = 20)
CAD_Input.place(x=750, y=118)

# ::: Mesh FILES NAMES TEXT :::
CAD_label = tk.Label(root, text="Add Mesh File names here", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
CAD_label.place(x=753, y=148)

# ::: PATH TO Mesh FOLDER INPUT FIELD :::
CAD_Folder_Input = tk.Entry(root, width = 20)
CAD_Folder_Input.place(x=750, y=180)

# ::: PATH TO Mesh FOLDER TEXT :::
CAD_Folder_Label = tk.Label(root, text="Enter the Mesh files folder path:", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
CAD_Folder_Label.place(x=753, y=210)




# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::             N A M I N G    N E W    G E O M E T R Y            :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# ::: GEOMETRY NAME TITLE :::
GeomName_label = tk.Label(root, text="Geometry Name", font=("Times New Roman", 15), bg="#F5F5F5", fg="black", width=23, anchor="center", justify="center")
GeomName_label.place(x=751, y=310)

# ::: GEOMETRY NAME INPUT FIELD :::
GeometryName = tk.Entry(root, width = 20)
GeometryName.place(x=750, y=340)

# ::: NAME OF THE GEOMETRY TEXT :::
geometry_label = tk.Label(root, text="Name your defined geometry", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
geometry_label.place(x=753, y=370)



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::           H O R I Z O N T A L    S E C T I O N S               :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# :::::: SHAPE ::::::
shape_label = tk.Label(root, text="Shape", font=("Times New Roman", 12), bg="#3D3D3D", fg="white")
shape_label.place(x=50, y=120)

# :::::: DIMENSIONS* ::::::
dimensions_label = tk.Label(root, text="Dimensions*", font=("Times New Roman", 12), bg="#3D3D3D", fg="white")
dimensions_label.place(x=50, y=180)

# ::: Box :::
Box_label = tk.Label(root, text="For Box:", font=("Times New Roman", 10), bg="#F5F5F5", fg="black")
Box_label.place(x=50, y=210)

# ::: Cylinder :::
Cylinder_label = tk.Label(root, text="For Cylinder:", font=("Times New Roman", 10), bg="#F5F5F5", fg="black")
Cylinder_label.place(x=50, y=233)

# :::::: POSITION ::::::
position_label = tk.Label(root, text="Position", font=("Times New Roman", 12), bg="#3D3D3D", fg="white")
position_label.place(x=50, y=270)

# :::::: MATERIAL ::::::
material_label = tk.Label(root, text="Material", font=("Times New Roman", 12), bg="#3D3D3D", fg="white")
material_label.place(x=50, y=340)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                      M A C R O    F I L E                      :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# :::::: MACRO FILE TEXT ::::::
Macro_label = tk.Label(root, text="Macro File", font=("Times New Roman", 15), bg="#F5F5F5", fg="black")
Macro_label.place(x=35, y=420)

# :::::: RADIOACTIV SOURCE TEXT ::::::
RadSource_label = tk.Label(root, text="Radioactive source", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
RadSource_label.place(x=122, y=420)

# :::::: ALPHA SOURCE SELECTION ::::::
radionuclide_combobox = ttk.Combobox(root, values=["ALPHA EMITTERS:", "Am-241", "Ra-224", "Pu-239", "Ra-226", "Ac-225", "Th-232", "Th-228", "U-238", "U-235", 
"At-211", "Po-210", "Cm-244", "Cf-252", "Rn-222", "BETA EMITTERS:", "Sr-90", "Y-90", "P-32", "S-35", "Lu-177", "Re-188", "Re-186", "Sm-153", "Ho-166", "I-131", "Ir-192", 
"Fe-59", "Na-24", "POSITRON EMITTERS:", "F-18", "C-11", "N-13", "O-15", "Ga-68", "Zr-89", "Cu-64", "Sc-44", "Rb-82", "Na-22", "I-124", "Y-86", "Br-76", 
"GAMMA EMITTERS:", "Tc-99m", "Co-57", "Co-60", "Cs-137", "Ba-133", "Mn-54", "Zn-65", "Fe-59", "Cd-109", "In-111", "Tl-201", "Xe-133", "Kr-85", "I-125"], state="readonly", font=("Times New Roman", 12), width = 27)
radionuclide_combobox.place(x=121, y=450)
radionuclide_combobox.set("Select Source")

# :::::: LOCATION OF THE SOURCE TEXT ::::::
Location_label = tk.Label(root, text="Location of radioactivity on the source", font=("Times New Roman", 12), bg="#F5F5F5", fg="black")
Location_label.place(x=405, y=420)

radionuclide_location_combobox = ttk.Combobox(root, values=["Volume", "Surface", "Point", "Beam"], state="readonly", font=("Times New Roman", 12))
radionuclide_location_combobox.place(x=425, y=450)
radionuclide_location_combobox.set("Select location")

# :::::: NUMBER OF RUNS ::::::
Runs_label = tk.Label(root, text="Number of runs", font=("Times New Roman", 12), bg="#F5F5F5", fg="black", width=30, anchor="center", justify="center")
Runs_label.place(x=753, y=420)

RunsInput = tk.Entry(root, width = 20)
RunsInput.place(x=750, y=450)



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                        B U T T O N S                           :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# :::::: LOAD GEOMETRY BUTTON ::::::
#load_geometry_button = tk.Button(root, text="Load Geometry", command=load_geometry)
#load_geometry_button.place(x=890, y = 540)

# :::::: SAVE BUTTON ::::::
save_canvas = tk.Canvas(root, width=80, height=30, bg=blue_color, highlightthickness=0)
save_button = save_canvas.create_text(40, 15, text="Save", fill="white", font=("Times New Roman", 10, "bold"))
save_canvas.place(x=490, y=540, anchor=tk.SE)


def save_click(event):
    save_input()          # Saves all the inputs to the click

save_canvas.bind("<Button-1>", save_click)


# :::::: CLOSE BUTTON ::::::
close_canvas = tk.Canvas(root, width=80, height=30, bg=blue_color, highlightthickness=0)
close_button = close_canvas.create_text(40, 15, text="Close", fill="white", font=("Times New Roman", 10, "bold"))
close_canvas.place(x=590, y=540, anchor=tk.SE)

def close_click(event):
    close_window()        # Closes the window to the click

close_canvas.bind("<Button-1>", close_click)

# Start the GUI event loop
root.mainloop()
