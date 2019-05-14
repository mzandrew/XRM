//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
//
/// \file B1DetectorConstruction.cc
/// \brief Implementation of the B1DetectorConstruction class

#include "B1DetectorConstruction.hh"

#include "G4RunManager.hh"
#include "G4NistManager.hh"
#include "G4SubtractionSolid.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4Cons.hh"
#include "G4Orb.hh"
#include "G4Sphere.hh"
#include "G4Trd.hh"
#include "G4LogicalVolume.hh"
#include "sensitiveObject.hh"
//#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1DetectorConstruction::B1DetectorConstruction()
: G4VUserDetectorConstruction(),
  fScoringVolume(0)
{ }

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1DetectorConstruction::~B1DetectorConstruction()
{ }

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
G4double z_position_of_gun;

#ifndef BULK_SI_SITUATION
#define REAL_XRM_SITUATION
#endif

#ifndef FACE_ON
#ifndef EDGE_ON
#define EDGE_ON
#endif
#endif

#ifndef LER
#ifndef HER
#define HER
#endif
#endif

#ifndef CEYAG
#ifndef LUAGCE
#define LUAGCE
#endif
#endif

G4VPhysicalVolume* B1DetectorConstruction::Construct() {
	// Get nist material manager
	G4NistManager* nist = G4NistManager::Instance();
	// SuperKEKB XRM:
	G4double vacuum_dimension = 20.*cm;
	#ifdef HER
	G4double Be_upstream_filter_dimension = 2.*mm; // since phase2 2.0 mm for HER; 0.5 mm for LER
	#endif
	#ifdef LER
	G4double Be_upstream_filter_dimension = 0.5*mm; // since phase2 2.0 mm for HER; 0.5 mm for LER
	#endif
//	G4double diamond_substrate_thickness = 800.*um; // since phase2
//	G4double gold_mask_thickness = 20.*um;
	G4double Be_window_dimension = 0.2*mm; // nominal; HER=8743/695/340 LER=21459/1282/860
//	G4double neck_dimension_of_box = 50.*mm + 108.*mm;
	G4double position_of_vacuum = 0. - vacuum_dimension/2. - Be_window_dimension;
	//G4double hypotenuse = sqrt(6.9**2.+14.**2.); // 15.61
	G4double env_diameter = 16.*mm;
	G4double object_radius = env_diameter/2. - 250.*um;
	#ifdef REAL_XRM_SITUATION
	G4double inside_dimension_of_box = 614.*mm;
	G4double position_of_Be_window = 0. - Be_window_dimension/2.;
	G4double position_of_He_envelope = inside_dimension_of_box/2.;
	G4double position_of_first_part_of_sensor = - inside_dimension_of_box/2. + 50.*cm; // nominal
	//G4double position_of_first_part_of_sensor = - inside_dimension_of_box/2. + 5.*cm; // in He, this doesn't seem to make a difference
	G4double env_sizeZ = inside_dimension_of_box;
	#endif
//	G4cout << "position_of_vacuum " << position_of_vacuum << G4endl;
//	G4cout << "position_of_Be_window " << position_of_Be_window << G4endl;
//	G4cout << "position_of_He_envelope " << position_of_He_envelope << G4endl;
//	G4cout << "position_of_first_part_of_sensor " << position_of_first_part_of_sensor << G4endl;
	// Option to switch on/off checking of volumes overlaps
	G4bool checkOverlaps = true;
	z_position_of_gun = position_of_vacuum - vacuum_dimension/2. + 1.*cm;
	G4double position_of_Be_filter = 0. + vacuum_dimension/2. - 10.*cm; // downstream of bulk_si reference
	G4double position_of_mask = 0. + vacuum_dimension/2. - 5.*cm; // downstream of bulk_si reference
	sensitiveObject *objet;
	G4int ncomponents;

	// World
	G4double world_sizeXY = 5.0*env_diameter;
	G4double world_sizeZ  = 2.*650.*mm;
	G4Material* world_mat = nist->FindOrBuildMaterial("G4_AIR");
	G4Box* solidWorld = new G4Box("World", 0.5*world_sizeXY, 0.5*world_sizeXY, 0.5*world_sizeZ);
	G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld,          //its solid
	                      world_mat,           //its material
	                      "World");            //its name
	G4VPhysicalVolume* physWorld = 
	  new sensitiveObject(0,                     //no rotation
	                    G4ThreeVector(),       //at (0,0,0)
	                    logicWorld,            //its logical volume
	                    "Air",               //its name
	                    0,                     //its mother  volume
	                    false,                 //no boolean operation
	                    0,                     //copy number
	                    checkOverlaps);        //overlaps checking
	sensitiveObjectVector.push_back((sensitiveObject*) physWorld);

	// beam pipe
	G4Material* vac_mat = nist->FindOrBuildMaterial("G4_Galactic");
	G4Tubs* solidVac = new G4Tubs("BeamPipeVac", 0., 0.5*env_diameter, 0.5*vacuum_dimension, 0., 2.*M_PI);
	G4LogicalVolume* logicVac = new G4LogicalVolume(solidVac,            //its solid
	                      vac_mat,             //its material
	                      "BeamPipeVac");         //its name
	G4ThreeVector pos_vac = G4ThreeVector(0, 0, position_of_vacuum);
	objet = new sensitiveObject(0,                       //no rotation
	                  pos_vac,
	                  logicVac,                //its logical volume
	                  "BeamPipeVacuum",              //its name
	                  logicWorld,              //its mother  volume
	                  false,                   //no boolean operation
	                  0,                       //copy number
	                  checkOverlaps);          //overlaps checking

	// all Be cylinders:
	G4Material* Be_mat = nist->FindOrBuildMaterial("G4_Be");
	G4double shape0_rmina =  0.*cm, shape0_rmaxa = object_radius;
	G4double shape0_rminb =  0.*cm, shape0_rmaxb = object_radius;
	G4double shape0_phimin = 0.*deg, shape0_phimax = 360.*deg;

	G4Material* Si_mat = nist->FindOrBuildMaterial("G4_Si");

	G4String name = "nothing";
	G4RotationMatrix *yRot = new G4RotationMatrix; // Rotates X and Z axes only
	yRot->rotateY(M_PI/4.*rad);

	// Be filter, upstream of mask:
	G4double shape5_hz = Be_upstream_filter_dimension/2.;
	G4ThreeVector pos0 = G4ThreeVector(0, 0, position_of_Be_filter);
	G4Cons* solidshape5 = new G4Cons("shape5", shape0_rmina, shape0_rmaxa, shape0_rminb, shape0_rmaxb, shape5_hz, shape0_phimin, shape0_phimax);
	G4LogicalVolume* logicshape5 = new G4LogicalVolume(solidshape5,         //its solid
	                      Be_mat,          //its material
	                      "shape5");           //its name
	objet = new sensitiveObject(0,                       //no rotation
	                  pos0,                    //at position
	                  logicshape5,             //its logical volume
	                  "BeFilter",                //its name
	                  logicVac,                //its mother  volume
	                  false,                   //no boolean operation
	                  0,                       //copy number
	                  checkOverlaps);          //overlaps checking
	sensitiveObjectVector.push_back(objet);

	// diamond substrate for mask
	name = "diamond";
	G4double diamond_sizeZ = 800.*um;
	G4Material *carbon = nist->FindOrBuildMaterial("G4_C");
	G4double density_diamond = 3.5*g/cm3;
	G4Material *diamond_mat = new G4Material(name,density_diamond,ncomponents=1);
	diamond_mat->AddMaterial(carbon,100.*perCent);
	G4ThreeVector diamond_pos = G4ThreeVector(0, 0, position_of_mask+diamond_sizeZ/2.);
	G4Tubs *diamond_solid = new G4Tubs(name, 0., object_radius, 0.5*diamond_sizeZ, 0., 2.*M_PI);
	G4LogicalVolume *diamond_logical_volume = new G4LogicalVolume(diamond_solid,         //its solid
	                      diamond_mat,          //its material
	                      name);           //its name
	objet = new sensitiveObject(0,                       //no rotation
	                  diamond_pos,                    //at position
	                  diamond_logical_volume,             //its logical volume
	                  name,                //its name
	                  logicVac,                //its mother  volume
	                  false,                   //no boolean operation
	                  0,                       //copy number
	                  checkOverlaps);          //overlaps checking
	sensitiveObjectVector.push_back(objet);

	#ifdef MASK_FULL
	// full gold for mask
	name = "gold";
	G4double gold_sizeZ = 20.*um;
	G4Material *gold_mat = nist->FindOrBuildMaterial("G4_Au");
	G4ThreeVector gold_pos = G4ThreeVector(0, 0, position_of_mask-gold_sizeZ/2.);
	G4Tubs *gold_solid = new G4Tubs(name, 0., object_radius, 0.5*gold_sizeZ, 0., 2.*M_PI);
	G4LogicalVolume *gold_logical_volume = new G4LogicalVolume(gold_solid,         //its solid
	                      gold_mat,          //its material
	                      name);           //its name
	objet = new sensitiveObject(0,                       //no rotation
	                  gold_pos,                    //at position
	                  gold_logical_volume,             //its logical volume
	                  name,                //its name
	                  logicVac,                //its mother  volume
	                  false,                   //no boolean operation
	                  0,                       //copy number
	                  checkOverlaps);          //overlaps checking
	sensitiveObjectVector.push_back(objet);
	#endif

	#ifdef REAL_XRM_SITUATION
		// select real XRM situation or bulk silicon
		pos0 = G4ThreeVector(0, 0, position_of_Be_window);
		G4double shape0_hz = Be_window_dimension/2.;
		G4Cons* solidshape0 = new G4Cons("shape0", shape0_rmina, shape0_rmaxa, shape0_rminb, shape0_rmaxb, shape0_hz, shape0_phimin, shape0_phimax);
		G4LogicalVolume* logicshape0 = new G4LogicalVolume(solidshape0,         //its solid
		                      Be_mat,          //its material
		                      "shape0");           //its name
		objet = new sensitiveObject(0,                       //no rotation
		                  pos0,                    //at position
		                  logicshape0,             //its logical volume
		                  "BeWindow",                //its name
		                  logicWorld,                //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
		sensitiveObjectVector.push_back(objet);
		// Envelope
		G4Material* env_mat = nist->FindOrBuildMaterial("G4_He"); // nominal; HER=8743/695/340 LER=21459/1282/860
		//G4Material* env_mat = nist->FindOrBuildMaterial("G4_AIR"); // suppression; HER=8743/447/162 LER=21459/597/268
		G4Tubs *solidEnv = new G4Tubs("Envelope", 0., env_diameter/2., 0.5*env_sizeZ, 0., 2.*M_PI);
		G4LogicalVolume *logicEnv = new G4LogicalVolume(solidEnv,            //its solid
		                      env_mat,             //its material
		                      "Envelope");         //its name
		G4ThreeVector env_pos = G4ThreeVector(0, 0, position_of_He_envelope);
		objet = new sensitiveObject(0,                       //no rotation
		                  env_pos,
		                  logicEnv,                //its logical volume
		                  "HeBox",              //its name
		                  logicWorld,              //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
		sensitiveObjectVector.push_back(objet);
//#define SCINTILLATOR_PRESENT
		#ifdef SCINTILLATOR_PRESENT
			G4int natoms;
			// from http://hypernews.slac.stanford.edu/HyperNews/geant4/get/phys-list/923.html
			G4double density_YAG = 4.56*g/cm3;
			G4Element *Al = nist->FindOrBuildElement("Al");
			G4Element *O = nist->FindOrBuildElement("O");
			G4Element *Ce = nist->FindOrBuildElement("Ce");
			#ifdef CEYAG
			G4Element *Y = nist->FindOrBuildElement("Y");
			G4Material *YAG = new G4Material("YAG",density_YAG,ncomponents=3);
			YAG->AddElement(Y,natoms=3);
			YAG->AddElement(Al,natoms=5);
			YAG->AddElement(O,natoms=12);
			G4double density_CeYAG = 4.55*g/cm3; // mulyani p56
			name = "Ce:YAG";
			G4Material *scint = new G4Material(name,density_CeYAG,ncomponents=2);
			scint->AddMaterial(YAG,98.2*perCent);
			scint->AddElement(Ce,1.8*perCent);
			#endif
			#ifdef LUAGCE
			// Lu3 Al5 O12
			G4Element *Lu = nist->FindOrBuildElement("Lu");
			G4Material *LuAG = new G4Material("LuAG",density_YAG,ncomponents=3);
			LuAG->AddElement(Lu,natoms=3);
			LuAG->AddElement(Al,natoms=5);
			LuAG->AddElement(O,natoms=12);
			G4double density_LuAGCe = 6.76*g/cm3; // mulyani p56
			name = "LuAG:Ce";
			G4Material *scint = new G4Material(name,density_LuAGCe,ncomponents=2);
			scint->AddMaterial(LuAG,99.7*perCent);
			scint->AddElement(Ce,0.3*perCent);
			#endif
			G4ThreeVector scintillator_pos = G4ThreeVector(0, 0, 20.*cm - env_sizeZ/2.);
			G4double scintillator_length = 100.*um;
			G4Tubs *scintillator_solidshape = new G4Tubs(name, 0., object_radius, scintillator_length/2., 0., 2.*M_PI);
			G4LogicalVolume *scintillator_logical_volume = new G4LogicalVolume(scintillator_solidshape, scint, name);
			objet = new sensitiveObject(yRot,
			                  scintillator_pos,                    //at position
			                  scintillator_logical_volume,             //its logical volume
			                  name,                //its name
			                  logicEnv,                //its mother  volume
			                  false,                   //no boolean operation
			                  0,                       //copy number
			                  checkOverlaps);          //overlaps checking
			sensitiveObjectVector.push_back(objet);
		#endif
//#define COPPER_BLOCKER_ON
		#ifdef COPPER_BLOCKER_ON
			// select edge-on or face-on
			// edge-on
			G4Material* copper_mat = nist->FindOrBuildMaterial("G4_Cu");
			G4ThreeVector copper1_pos = G4ThreeVector(0, 0, 45.*cm - env_sizeZ/2.);
			const G4String name = "copper1";
			//G4double copper1_length = 200.*um; // HER=8743/4/0 LER=21459/0/0
			//G4double copper1_length = 100.*um; // HER=8743/5/0 LER=21459/10/5
			//G4double copper1_length = 50.*um; // HER=8743/42/15 LER=21459/56/26
			G4double copper1_length = 25.*um; // HER=8743/123/44 LER=21459/148/79
			//G4double copper1_length = 0.*um; // HER=8743/690/339 LER=21459/1285/868
			G4Cons* copper1_solidshape = new G4Cons("shape4", shape0_rmina, shape0_rmaxa, shape0_rminb, shape0_rmaxb, copper1_length/2., shape0_phimin, shape0_phimax);
			G4LogicalVolume* copper_logical_volume = new G4LogicalVolume(copper1_solidshape, copper_mat, name);
			objet = new sensitiveObject(0,                       //no rotation
			                  copper1_pos,                    //at position
			                  copper_logical_volume,             //its logical volume
			                  name,                //its name
			                  logicEnv,                //its mother  volume
			                  false,                   //no boolean operation
			                  0,                       //copy number
			                  checkOverlaps);          //overlaps checking
			sensitiveObjectVector.push_back(objet);
		#endif
#define COPPER_SLIT_ON
		#ifdef COPPER_SLIT_ON
			// select edge-on or face-on
			// edge-on
			G4Material* copper_mat = nist->FindOrBuildMaterial("G4_Cu");
			G4ThreeVector copper_slit1_pos = G4ThreeVector(0, 0, 45.*cm - env_sizeZ/2.);
			name = "CopperSlit";
			//G4double copper1_length = 200.*um; // HER=8743/4/0 LER=21459/0/0
			//G4double copper1_length = 100.*um; // HER=8743/5/0 LER=21459/10/5
			//G4double copper1_length = 50.*um; // HER=8743/42/15 LER=21459/56/26
			G4double copper_slit1_length = 9.525*mm; // HER=8743/123/44 LER=21459/148/79
			//G4double copper1_length = 0.*um; // HER=8743/690/339 LER=21459/1285/868
			G4Tubs *copper_slit1_cyl_solidshape = new G4Tubs("copper_slit1_cyl", 0., object_radius, copper_slit1_length/2., 0., 2.*M_PI);
			G4Box *copper_slit1_box_solidshape = new G4Box("copper_slit1_box", 75.*um/2., 14.*mm/2., copper_slit1_length);
			G4VSolid *copper_slit1_solidshape = new G4SubtractionSolid("copper_slit1", copper_slit1_cyl_solidshape, copper_slit1_box_solidshape, 0, G4ThreeVector(0., 0., 0.));
			G4LogicalVolume *copper_slit1_logical_volume = new G4LogicalVolume(copper_slit1_solidshape, copper_mat, name);
			objet = new sensitiveObject(0,                       //no rotation
			                  copper_slit1_pos,                    //at position
			                  copper_slit1_logical_volume,             //its logical volume
			                  name,                //its name
			                  logicEnv,                //its mother  volume
			                  false,                   //no boolean operation
			                  0,                       //copy number
			                  checkOverlaps);          //overlaps checking
			sensitiveObjectVector.push_back(objet);
		#endif
		#ifdef EDGE_ON
			// select edge-on or face-on
			// edge-on
			G4Material* shape1_mat = nist->FindOrBuildMaterial("G4_Si");
			G4double position_of_edge_on_sensor = position_of_first_part_of_sensor + 2.*mm/2.;
			G4ThreeVector pos1 = G4ThreeVector(0, 0, position_of_edge_on_sensor);
			// Trapezoid shape       
			G4double shape1_dxa = 75.*um, shape1_dxb = 75.*um;
			G4double shape1_dya = 6.*mm, shape1_dyb = 6.*mm;
			G4double shape1_dz  = 2.*mm;
			G4Trd* solidShape1 = new G4Trd("Shape1",                      //its name
			            0.5*shape1_dxa, 0.5*shape1_dxb, 
			            0.5*shape1_dya, 0.5*shape1_dyb, 0.5*shape1_dz); //its size
			G4LogicalVolume* logicShape1 = new G4LogicalVolume(solidShape1,         //its solid
			                      shape1_mat,          //its material
			                      "Shape1");           //its name
			objet = new sensitiveObject(0,                       //no rotation
			                  pos1,                    //at position
			                  logicShape1,             //its logical volume
			                  "SiEdgeOn",                //its name
			                  logicEnv,                //its mother  volume
			                  false,                   //no boolean operation
			                  0,                       //copy number
			                  checkOverlaps);          //overlaps checking
			sensitiveObjectVector.push_back(objet);
			// Set as scoring volume
			fScoringVolume = logicShape1;
		#endif
		#ifdef FACE_ON
			// face-on
			G4Material* shape2_mat = nist->FindOrBuildMaterial("G4_Si");
			G4double position_of_face_on_sensor = position_of_first_part_of_sensor + 75.*um/2.;
			G4ThreeVector pos2 = G4ThreeVector(0, 0, position_of_face_on_sensor);
			// Trapezoid shape       
			G4double shape2_dxa = 75.*um, shape2_dxb = 75.*um;
			G4double shape2_dya = 6.*mm, shape2_dyb = 6.*mm;
			G4double shape2_dz  = 2.*mm;
			G4Trd* solidShape2 = new G4Trd("Shape2",                      //its name
			            0.5*shape2_dxa, 0.5*shape2_dxb, 
			            0.5*shape2_dya, 0.5*shape2_dyb, 0.5*shape2_dz); //its size
			G4LogicalVolume* logicShape2 = new G4LogicalVolume(solidShape2,         //its solid
			                      shape2_mat,          //its material
			                      "Shape2");           //its name
			G4RotationMatrix *yRot2 = new G4RotationMatrix; // Rotates X and Z axes only
			yRot2->rotateY(M_PI/2.*rad);
			objet = new sensitiveObject(yRot2,                   //rotation
			                  pos2,                    //at position
			                  logicShape2,             //its logical volume
			                  "SiFaceOn",                //its name
			                  logicEnv,                //its mother  volume
			                  false,                   //no boolean operation
			                  0,                       //copy number
			                  checkOverlaps);          //overlaps checking
			sensitiveObjectVector.push_back(objet);
			// Set as scoring volume
			fScoringVolume = logicShape2;
		#endif
	// Si beamdump downstream
		G4double beamdump_Si_dz = 6.*mm;
		G4double position_of_beamdump_Si = inside_dimension_of_box + beamdump_Si_dz/2.;
		G4ThreeVector pos6 = G4ThreeVector(0, 0, position_of_beamdump_Si);
		G4Tubs* beamdump_Si_solidshape = new G4Tubs("beamdump", 0., object_radius, 0.5*beamdump_Si_dz, 0., 2.*M_PI);
		G4LogicalVolume* beamdump_Si_logical_volume = new G4LogicalVolume(beamdump_Si_solidshape,         //its solid
		                      Si_mat,          //its material
		                      "beamdump");           //its name
		objet = new sensitiveObject(0,                       //rotation
		                  pos6,                    //at position
		                  beamdump_Si_logical_volume, //its logical volume
		                  "SiBeamDump",                //its name
		                  logicWorld,                //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
		sensitiveObjectVector.push_back(objet);
		// Set as scoring volume
		//fScoringVolume = beamdump_Si_logical_volume;
	#endif

	#ifdef BULK_SI_SITUATION
		// Si bulk
		G4double shape3_dz = 6.*mm;
		//G4double position_of_bulk_sensor = position_of_first_part_of_sensor + shape3_dz/2.;
		//G4double position_of_bulk_sensor = position_of_vacuum;
		G4double position_of_bulk_sensor = 0. - 5*cm;
		//G4double position_of_bulk_sensor = - inside_dimension_of_box/2.;
		G4ThreeVector pos3 = G4ThreeVector(0, 0, position_of_bulk_sensor);
		G4Tubs* solidShape3 = new G4Tubs("Envelope", 0., object_radius, 0.5*shape3_dz, 0., 2.*M_PI);
		G4LogicalVolume* logicShape3 = new G4LogicalVolume(solidShape3,         //its solid
		                      Si_mat,          //its material
		                      "Envelope");           //its name
		objet = new sensitiveObject(0,                       //rotation
		                  pos3,                    //at position
		                  logicShape3,             //its logical volume
		                  "SiBulk",                //its name
		                  logicVac,                //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
		sensitiveObjectVector.push_back(objet);
		// Set as scoring volume
		fScoringVolume = logicShape3;
	#endif

	//always return the physical World
	return physWorld;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

