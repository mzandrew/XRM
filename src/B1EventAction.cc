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
/// \file B1EventAction.cc
/// \brief Implementation of the B1EventAction class

#include "B1EventAction.hh"
#include "B1RunAction.hh"

#include "G4Event.hh"
#include "G4MTRunManager.hh"
#include <iterator>
#include "B1DetectorConstruction.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1EventAction::B1EventAction(B1RunAction* runAction) : G4UserEventAction(), fRunAction(runAction), fEdep(0.) {
//	G4cout << "B1EventAction constructor called" << G4endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1EventAction::~B1EventAction() {
//	G4cout << "B1EventAction default constructor called" << G4endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void B1EventAction::BeginOfEventAction(const G4Event*) {
//	G4cout << "BeginOfEventAction called" << G4endl;
  fEdep = 0.;
	B1DetectorConstruction *detector = (B1DetectorConstruction*) G4MTRunManager::GetRunManager()->GetUserDetectorConstruction();
	for (std::vector<sensitiveObject*>::iterator i=detector->sensitiveObjectVector.begin(); i!=detector->sensitiveObjectVector.end(); i++) {
		(*i)->clearDepositedEnergy();
	}
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

const float epsilon = 1.e-3*CLHEP::eV;
//const float silicon_work_function = epsilon;
//const G4double silicon_work_function = 4.91*CLHEP::eV;
void B1EventAction::EndOfEventAction(const G4Event*) {
	B1DetectorConstruction *detector = (B1DetectorConstruction*) G4MTRunManager::GetRunManager()->GetUserDetectorConstruction();
	for (std::vector<sensitiveObject*>::iterator i=detector->sensitiveObjectVector.begin(); i!=detector->sensitiveObjectVector.end(); i++) {
		G4double energy_deposited = (*i)->getDepositedEnergy();
		if (energy_deposited > epsilon) {
			G4String name = (*i)->GetName();
			G4cout << " " << energy_deposited/CLHEP::eV << " " << name;
		}
	}
	G4cout << G4endl;
	return;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

