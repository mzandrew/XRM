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
/// \file B1PrimaryGeneratorAction.cc
/// \brief Implementation of the B1PrimaryGeneratorAction class

#include "B1PrimaryGeneratorAction.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4RunManager.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"
#include "Randomize.hh"
#include "G4SynchrotronRadiation.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1PrimaryGeneratorAction::B1PrimaryGeneratorAction()
: G4VUserPrimaryGeneratorAction(), fParticleGun(0), fEnvelopeBox(0)
{
//	G4cout << "B1PrimaryGeneratorAction constructor called" << G4endl;
	G4int n_particle = 1;
	fParticleGun = new G4ParticleGun(n_particle);
	// default particle kinematic
	G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
	G4String particleName;
	G4ParticleDefinition *particle = particleTable->FindParticle(particleName="gamma");
	fParticleGun->SetParticleDefinition(particle);
	fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0.,0.,1.));
	fParticleGun->SetParticleEnergy(10.*keV);
//	G4UImanager* UI = G4UImanager::GetUIpointer();
//	UI->ApplyCommand("/control/alias critial_energy 10. keV");
	G4double x0 = 0.*mm;
	G4double y0 = 0.*mm;
	G4double z0 = -200.*mm;
	G4ThreeVector pos;
	pos.set(x0, y0, z0);
	fParticleGun->SetParticlePosition(pos);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

B1PrimaryGeneratorAction::~B1PrimaryGeneratorAction() {
  delete fParticleGun;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4double ln(G4double value) {
	return log(value);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4double InvSynFracInt(G4double y) {
// after Burkhardt MONTE CARLO GENERATION OF THE ENERGY SPECTRUM OF SYNCHROTRON RADIATION
	G4double x = 0.0;
	const G4double y1 = 0.7;
	const G4double y2 = 0.91322603;
	const G4double g1 = pow(y1, 3.);
	const G4double g2 = -ln(1.-y2);
	const G4double slope = (g2-g1) / (y2-y1);
	     if (y<y1) { x = pow(y, 3.); }
	else if (y>y2) { x = -ln(1.-y); }
	else           { x = slope * (y-y1) + g1; }
	return x;
//	return y;
//	return 1.;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
extern G4double z_position_of_gun;
G4int event_counter = 0;

void B1PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent) {
//	G4cout << "GeneratePrimaries called" << G4endl;
	//this function is called at the begining of each event
	// In order to avoid dependence of PrimaryGeneratorAction
	// on DetectorConstruction class we get Envelope volume
	// from G4LogicalVolumeStore.
	if (!fEnvelopeBox) {
		G4LogicalVolume* envLV = G4LogicalVolumeStore::GetInstance()->GetVolume("Envelope");
		if ( envLV ) fEnvelopeBox = dynamic_cast<G4Box*>(envLV->GetSolid());
	}
	G4ThreeVector pos;
	pos = fParticleGun->GetParticlePosition();
	#ifdef HER
		G4double beam_vertical_size = 6.5*mm; 
	#endif
	#ifdef LER
		G4double beam_vertical_size = 6.9*mm; 
	#endif
	G4double y0 = beam_vertical_size * (G4UniformRand()-0.5);
	G4double z0 = z_position_of_gun;
	pos.setY(y0);
	pos.setZ(z0);
	fParticleGun->SetParticlePosition(pos);
	static G4float critial_energy = fParticleGun->GetParticleEnergy();
//	G4float critial_energy = 7.18*keV; // HER
//	G4float critial_energy = 4.458*keV; // LER
	G4double q = G4UniformRand();
	G4SynchrotronRadiation a;
	G4double w = a.G4SynchrotronRadiation::InvSynFracInt(q);
	G4double energy = critial_energy*w;
	fParticleGun->SetParticleEnergy(energy);
	//G4cout << "energy of photon: " << energy/CLHEP::keV << " keV" << G4endl;
	fParticleGun->GeneratePrimaryVertex(anEvent); // this line actually fires the photon...
	event_counter++;
	G4cout << event_counter << " " << std::setw(12) << energy/CLHEP::keV;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

