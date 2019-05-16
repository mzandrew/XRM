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
/// \file B1SteppingAction.cc
/// \brief Implementation of the B1SteppingAction class

#include "B1SteppingAction.hh"
#include "B1EventAction.hh"
#include "B1DetectorConstruction.hh"

#include "G4Step.hh"
#include "G4Event.hh"
#include "G4RunManager.hh"
#include "sensitiveObject.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1SteppingAction::B1SteppingAction(B1EventAction* eventAction)
: G4UserSteppingAction(),
  fEventAction(eventAction),
  fScoringVolume(0)
{
//	G4cout << "B1SteppingAction constructor called" << G4endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1SteppingAction::~B1SteppingAction()
{
//	G4cout << "B1SteppingAction destructor called" << G4endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

const float epsilon = 1.e-3*CLHEP::eV;
void B1SteppingAction::UserSteppingAction(const G4Step* step) {
	const G4VProcess *process = step->GetPostStepPoint()->GetProcessDefinedStep();
	G4String name = process->GetProcessName();
	// collect energy deposited in this step
	G4double edepStep = step->GetTotalEnergyDeposit();
	if ("Transportation" != name && edepStep > epsilon) {
		G4cout << " " << edepStep/CLHEP::eV << " " << name;
	}
	sensitiveObject *object = (sensitiveObject*) step->GetPreStepPoint()->GetTouchableHandle()->GetVolume();
//	G4cout << " [" << object->getDepositedEnergy()/CLHEP::eV;
	object->accumulateDepositedEnergy(edepStep);
//	G4cout << "," << object->getDepositedEnergy()/CLHEP::eV << "] " << name;
	//	G4cout << "UserSteppingAction called" << G4endl;
	return;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

