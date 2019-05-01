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
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4Cons.hh"
#include "G4Orb.hh"
#include "G4Sphere.hh"
#include "G4Trd.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
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

G4VPhysicalVolume* B1DetectorConstruction::Construct() {
	// Get nist material manager
	G4NistManager* nist = G4NistManager::Instance();
	// SuperKEKB XRM:
	G4double vacuum_dimension = 10.*cm;
	G4double Be_window_dimension_1 = 2.*mm;
	G4double Be_window_dimension_2 = 2.*mm;
	G4double air_gap_dimension = 10.*cm;
	//G4double wall_thickness_of_box = 3.*mm;
	G4double inside_dimension_of_box = 614.*mm; // D8 LER
//	G4double neck_dimension_of_box = 50.*mm + 108.*mm;
	// Envelope parameters
	G4double position_of_vacuum = 0. - vacuum_dimension/2. - Be_window_dimension_1 - air_gap_dimension - Be_window_dimension_2;
	G4double position_of_Be_window_1 = 0. - Be_window_dimension_1/2. - air_gap_dimension - Be_window_dimension_2;
	G4double position_of_Be_window_2 = 0. - Be_window_dimension_2/2.;
	G4double position_of_He_envelope = inside_dimension_of_box/2.;
	G4double position_of_first_part_of_sensor = - inside_dimension_of_box/2. + 500.*mm;
//	G4cout << "position_of_vacuum " << position_of_vacuum << G4endl;
//	G4cout << "position_of_Be_window_1 " << position_of_Be_window_1 << G4endl;
//	G4cout << "position_of_He_envelope " << position_of_He_envelope << G4endl;
//	G4cout << "position_of_first_part_of_sensor " << position_of_first_part_of_sensor << G4endl;
	G4double env_diameter = 8.5*mm, env_sizeZ = inside_dimension_of_box;
	// Option to switch on/off checking of volumes overlaps
	G4bool checkOverlaps = true;

	// World
	G4double world_sizeXY = 1.2*env_diameter;
	G4double world_sizeZ  = 2.*650.*mm;
	G4Material* world_mat = nist->FindOrBuildMaterial("G4_AIR");
	G4Box* solidWorld = new G4Box("World",                       //its name
	     0.5*world_sizeXY, 0.5*world_sizeXY, 0.5*world_sizeZ);     //its size
	G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld,          //its solid
	                      world_mat,           //its material
	                      "World");            //its name
	G4VPhysicalVolume* physWorld = 
	  new G4PVPlacement(0,                     //no rotation
	                    G4ThreeVector(),       //at (0,0,0)
	                    logicWorld,            //its logical volume
	                    "World",               //its name
	                    0,                     //its mother  volume
	                    false,                 //no boolean operation
	                    0,                     //copy number
	                    checkOverlaps);        //overlaps checking

	// beam pipe
	G4Material* vac_mat = nist->FindOrBuildMaterial("G4_Galactic");
	G4Tubs* solidVac = new G4Tubs("BeamPipeVac", 0., 0.5*env_diameter, 0.5*vacuum_dimension, 0., 2.*M_PI);
	G4LogicalVolume* logicVac = new G4LogicalVolume(solidVac,            //its solid
	                      vac_mat,             //its material
	                      "BeamPipeVac");         //its name
	G4ThreeVector pos_vac = G4ThreeVector(0, 0, position_of_vacuum);
	new G4PVPlacement(0,                       //no rotation
	                  pos_vac,
	                  logicVac,                //its logical volume
	                  "BeamPipeVac",              //its name
	                  logicWorld,              //its mother  volume
	                  false,                   //no boolean operation
	                  0,                       //copy number
	                  checkOverlaps);          //overlaps checking

	#ifndef BULK_SI_SITUATION
	#define REAL_XRM_SITUATION
	#endif

	#ifndef FACE_ON
	#define EDGE_ON
	#endif

	G4Material* Be_mat = nist->FindOrBuildMaterial("G4_Be");
	#ifdef REAL_XRM_SITUATION
		// select real XRM situation or bulk silicon
		G4ThreeVector pos0 = G4ThreeVector(0, 0, position_of_Be_window_1);
		G4double shape0_rmina =  0.*cm, shape0_rmaxa = env_diameter/2.;
		G4double shape0_rminb =  0.*cm, shape0_rmaxb = env_diameter/2.;
		G4double shape0_hz = Be_window_dimension_1/2.;
		G4double shape0_phimin = 0.*deg, shape0_phimax = 360.*deg;
		G4Cons* solidshape0 = new G4Cons("shape0", 
		  shape0_rmina, shape0_rmaxa, shape0_rminb, shape0_rmaxb, shape0_hz,
		  shape0_phimin, shape0_phimax);
		G4LogicalVolume* logicshape0 = new G4LogicalVolume(solidshape0,         //its solid
		                      Be_mat,          //its material
		                      "shape0");           //its name
		new G4PVPlacement(0,                       //no rotation
		                  pos0,                    //at position
		                  logicshape0,             //its logical volume
		                  "shape0",                //its name
		                  logicWorld,                //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
		pos0 = G4ThreeVector(0, 0, position_of_Be_window_2);
		shape0_rmina =  0.*cm, shape0_rmaxa = env_diameter/2.;
		shape0_rminb =  0.*cm, shape0_rmaxb = env_diameter/2.;
		shape0_hz = Be_window_dimension_1/2.;
		shape0_phimin = 0.*deg, shape0_phimax = 360.*deg;
		G4Cons* solidshape4 = new G4Cons("shape4", 
		  shape0_rmina, shape0_rmaxa, shape0_rminb, shape0_rmaxb, shape0_hz,
		  shape0_phimin, shape0_phimax);
		G4LogicalVolume* logicshape4 = new G4LogicalVolume(solidshape4,         //its solid
		                      Be_mat,          //its material
		                      "shape4");           //its name
		new G4PVPlacement(0,                       //no rotation
		                  pos0,                    //at position
		                  logicshape4,             //its logical volume
		                  "shape4",                //its name
		                  logicWorld,                //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
		// Envelope
		G4Material* env_mat = nist->FindOrBuildMaterial("G4_He");
		G4Tubs *solidEnv = new G4Tubs("Envelope", 0., env_diameter/2., 0.5*env_sizeZ, 0., 2.*M_PI);
		G4LogicalVolume *logicEnv = new G4LogicalVolume(solidEnv,            //its solid
		                      env_mat,             //its material
		                      "Envelope");         //its name
		G4ThreeVector env_pos = G4ThreeVector(0, 0, position_of_He_envelope);
		new G4PVPlacement(0,                       //no rotation
		                  env_pos,
		                  logicEnv,                //its logical volume
		                  "Envelope",              //its name
		                  logicWorld,              //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
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
			new G4PVPlacement(0,                       //no rotation
			                  pos1,                    //at position
			                  logicShape1,             //its logical volume
			                  "Shape1",                //its name
			                  logicEnv,                //its mother  volume
			                  false,                   //no boolean operation
			                  0,                       //copy number
			                  checkOverlaps);          //overlaps checking
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
			new G4PVPlacement(yRot2,                   //rotation
			                  pos2,                    //at position
			                  logicShape2,             //its logical volume
			                  "Shape2",                //its name
			                  logicEnv,                //its mother  volume
			                  false,                   //no boolean operation
			                  0,                       //copy number
			                  checkOverlaps);          //overlaps checking
			// Set as scoring volume
			fScoringVolume = logicShape2;
		#endif
	#endif

	#ifdef BULK_SI_SITUATION
		// Si bulk
		G4Material* shape3_mat = nist->FindOrBuildMaterial("G4_Si");
		G4double shape3_dz = 6.*mm;
		//G4double position_of_bulk_sensor = position_of_first_part_of_sensor + shape3_dz/2.;
		//G4double position_of_bulk_sensor = position_of_vacuum;
		G4double position_of_bulk_sensor = 0.;
		//G4double position_of_bulk_sensor = - inside_dimension_of_box/2.;
		G4ThreeVector pos3 = G4ThreeVector(0, 0, position_of_bulk_sensor);
		G4Tubs* solidShape3 = new G4Tubs("Envelope", 0., env_diameter/2., 0.5*shape3_dz, 0., 2.*M_PI);
		G4LogicalVolume* logicShape3 = new G4LogicalVolume(solidShape3,         //its solid
		                      shape3_mat,          //its material
		                      "Envelope");           //its name
		new G4PVPlacement(0,                       //rotation
		                  pos3,                    //at position
		                  logicShape3,             //its logical volume
		                  "Envelope",                //its name
		                  logicVac,                //its mother  volume
		                  false,                   //no boolean operation
		                  0,                       //copy number
		                  checkOverlaps);          //overlaps checking
		// Set as scoring volume
		fScoringVolume = logicShape3;
	#endif


	//always return the physical World
	return physWorld;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

