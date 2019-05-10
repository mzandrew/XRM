#ifndef __SENSITIVEOBJECT_H__
#define __SENSITIVEOBJECT_H__

#include "G4PVPlacement.hh"

class sensitiveObject : public G4PVPlacement {
public:
	sensitiveObject(G4RotationMatrix *pRot, const G4ThreeVector &tlate, G4LogicalVolume *pCurrentLogical, const G4String& pName, G4LogicalVolume *pMotherLogical, G4bool pMany, G4int  pCopyNo, G4bool pSurfChk=false) : G4PVPlacement(pRot, tlate, pCurrentLogical, pName, pMotherLogical, pMany, pCopyNo, pSurfChk) {
		deposited_energy = 0.;
	}
	~sensitiveObject() {}
	inline G4double accumulateDepositedEnergy(G4double value) {
		deposited_energy += value;
		return deposited_energy;
	}
	inline G4double getDepositedEnergy(void) {
		return deposited_energy;
	}
	inline void clearDepositedEnergy(void) {
		deposited_energy = 0.;
	}
private:
	G4double deposited_energy;
};

#endif

