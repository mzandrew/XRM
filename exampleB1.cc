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
/// \file exampleB1.cc
/// \brief Main program of the B1 example

#include "B1DetectorConstruction.hh"
#include "B1ActionInitialization.hh"
#ifdef G4MULTITHREADED
#include "G4MTRunManager.hh"
#else
#include "G4RunManager.hh"
#endif
#include "G4UImanager.hh"
#include "QBBC.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"
#include "Randomize.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
extern G4int event_counter;

int main(int argc, char **argv)
{
  // Detect interactive mode (if no arguments) and define UI session
  G4UIExecutive* ui = 0;
  if ( argc == 1 ) {
    ui = new G4UIExecutive(argc, argv);
  }
  // Choose the Random engine
  G4Random::setTheEngine(new CLHEP::RanecuEngine);
  // Construct the default run manager
#ifdef G4MULTITHREADED
  G4MTRunManager* runManager = new G4MTRunManager;
#else
  G4RunManager* runManager = new G4RunManager;
#endif
  // Set mandatory initialization classes
  // Detector construction
  runManager->SetUserInitialization(new B1DetectorConstruction());
  // Physics list
  G4VModularPhysicsList* physicsList = new QBBC; // takes 70m for 191M photons
  physicsList->SetVerboseLevel(0);
  runManager->SetUserInitialization(physicsList);
  // User action initialization
  runManager->SetUserInitialization(new B1ActionInitialization());
  // Initialize visualization
  G4VisManager* visManager = new G4VisExecutive;
  // G4VisExecutive can take a verbosity argument - see /vis/verbose guidance.
  // G4VisManager* visManager = new G4VisExecutive("Quiet");
  visManager->Initialize();
  // Get the pointer to the User Interface manager
  G4UImanager* UImanager = G4UImanager::GetUIpointer();
  // from http://hypernews.slac.stanford.edu/HyperNews/geant4/get/phys-list/923/1/1.html
  UImanager->ApplyCommand("/gras/physics/addPhysics em_livermore");
  //UImanager->ApplyCommand("/gras/physics/addPhysics em_penelope");
  UImanager->ApplyCommand("/cuts/setLowEdge 4 eV");
  //UImanager->ApplyCommand("/gras/physics/productionCutsLowestEnergy 10 eV");
  UImanager->ApplyCommand("/process/em/fluo true");
  UImanager->ApplyCommand("/process/em/auger true");
  UImanager->ApplyCommand("/process/em/pixe true");
  //UImanager->ApplyCommand("/gras/physics/setCuts 0.1 um");
  //UImanager->ApplyCommand("/gras/physics/setGCut 1 nm");
  //UImanager->ApplyCommand("/gras/physics/setECut 1 nm");
  //UImanager->ApplyCommand("/run/setCut 10 nm");
  // Process macro or start UI session
  if ( ! ui ) { 
    // batch mode
    G4String command = "/control/execute ";
    G4String fileName = argv[1];
    UImanager->ApplyCommand(command+fileName);
  } else { 
    // interactive mode
    UImanager->ApplyCommand("/control/execute init_vis.mac");
    ui->SessionStart();
    delete ui;
  }
  // Job termination
  // Free the store: user actions, physics_list and detector_description are
  // owned and deleted by the run manager, so they should not be deleted 
  // in the main() program !
  delete visManager;
  delete runManager;
  G4cout << "completed " << event_counter << " events" << G4endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo.....

