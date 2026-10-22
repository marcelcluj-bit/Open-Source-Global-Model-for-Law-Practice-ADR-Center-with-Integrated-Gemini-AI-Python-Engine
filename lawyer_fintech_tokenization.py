"""
Legal Tech & Lawyer Fintech Tokenization Protocol (RWA)
-------------------------------------------------------
Open-Source Web3 Module for Tokenizing Legal Case Funding, 
Litigation Finance Crowdfunding, ADR Settlement Escrow, 
and Multi-Jurisdictional Lawyer Profit-Sharing.

License: MIT
"""

import time
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class LitigationFundToken:
    token_id: str
    investor_address: str
    case_id: str
    amount_funded_eur: float
    equity_yield_percentage: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class CaseEscrowVault:
    vault_id: str
    jurisdiction_code: str
    case_type: str  # "Litigation", "ADR_Mediation", "Commercial_Conciliation"
    total_claim_amount_eur: float
    agreed_contingency_fee_percent: float
    escrowed_funds_eur: float
    is_settled: bool = False
    is_disputed: bool = False

class LegalFintechTokenEngine:
    """
    Decentralized Finance (DeFi) & RWA Engine for Law Firms & ADR Centers.
    Enables cross-border crowdfunding for high-stake litigation and automated
    settlement distribution via Smart Escrow Contracts.
    """
    def __init__(self, platform_name: str = "Global-Legal-ADR-Network"):
        self.platform_name = platform_name
        self.funding_tokens: Dict[str, LitigationFundToken] = {}
        self.escrow_vaults: Dict[str, CaseEscrowVault] = {}
        self.total_litigation_funded_eur: float = 0.0
        self.total_adr_settled_eur: float = 0.0

    def create_case_vault(self, vault_id: str, jurisdiction: str, case_type: str, claim_val: float, fee_percent: float = 15.0) -> CaseEscrowVault:
        """Registers a new legal case or ADR procedure into the tokenized smart escrow system."""
        vault = CaseEscrowVault(
            vault_id=vault_id,
            jurisdiction_code=jurisdiction,
            case_type=case_type,
            total_claim_amount_eur=claim_val,
            agreed_contingency_fee_percent=fee_percent,
            escrowed_funds_eur=0.0
        )
        self.escrow_vaults[vault_id] = vault
        print(f"[VAULT CREATED] ID: {vault_id} | Jurisdiction: {jurisdiction} | Claim: €{claim_val:,.2f} | Fee: {fee_percent}%")
        return vault

    def fund_litigation_case(self, investor_address: str, vault_id: str, funding_amount_eur: float) -> Optional[LitigationFundToken]:
        """Allows global micro-investors or litigation funds to finance legal/ADR costs in exchange for a share of success fees."""
        if vault_id not in self.escrow_vaults:
            print(f"[ERROR] Case Vault {vault_id} not found.")
            return None

        vault = self.escrow_vaults[vault_id]
        token_id = hashlib.sha256(f"{investor_address}_{vault_id}_{time.time()}".encode()).hexdigest()[:12]
        
        # Calculate yield share based on contribution
        yield_share = (funding_amount_eur / vault.total_claim_amount_eur) * vault.agreed_contingency_fee_percent

        token = LitigationFundToken(
            token_id=token_id,
            investor_address=investor_address,
            case_id=vault_id,
            amount_funded_eur=funding_amount_eur,
            equity_yield_percentage=yield_share
        )
        
        self.funding_tokens[token_id] = token
        self.total_litigation_funded_eur += funding_amount_eur
        print(f"[FUNDING TOKEN ISSUED] Investor {investor_address[:8]}... funded €{funding_amount_eur:,.2f} for Case {vault_id}")
        return token

    def deposit_escrow_settlement(self, vault_id: str, settlement_amount_eur: float):
        """Deposits final mediated settlement or court award funds into the smart contract vault."""
        if vault_id in self.escrow_vaults:
            vault = self.escrow_vaults[vault_id]
            vault.escrowed_funds_eur += settlement_amount_eur
            print(f"[ESCROW DEPOSIT] €{settlement_amount_eur:,.2f} deposited into Vault {vault_id}")

    def execute_adr_settlement_payout(self, vault_id: str, local_lawyer_payout_address: str):
        """Executes automated smart payout upon successful mediation/arbitration agreement."""
        if vault_id not in self.escrow_vaults:
            print(f"[ERROR] Vault {vault_id} not found.")
            return

        vault = self.escrow_vaults[vault_id]
        if vault.is_settled:
            print(f"[WARNING] Vault {vault_id} is already settled.")
            return

        vault.is_settled = True
        total_payout = vault.escrowed_funds_eur
        total_fee = total_payout * (vault.agreed_contingency_fee_percent / 100.0)
        client_payout = total_payout - total_fee

        self.total_adr_settled_eur += total_payout

        print("\n" + "="*70)
        print(f"      SMART ESCROW EXECUTION & ADR SETTLEMENT PAYOUT: {vault_id}")
        print("="*70)
        print(f"Jurisdiction: {vault.jurisdiction_code}")
        print(f"Total Settled Amount: €{total_payout:,.2f}")
        print(f" -> Client Payout (Net): €{client_payout:,.2f}")
        print(f" -> Total Success Commission (Lawyer + Token Fund): €{total_fee:,.2f}")

        # Distribute yields to litigation token holders
        lawyer_commission = total_fee * 0.70  # 70% to local jurisdiction lawyers
        token_pool_yield = total_fee * 0.30   # 30% to global litigation fund investors

        print(f" -> Local Lawyer Partner ({local_lawyer_payout_address[:8]}...): €{lawyer_commission:,.2f}")
        print(f" -> Distributing €{token_pool_yield:,.2f} to Litigation Crowdfund Investors:")

        for tid, token in self.funding_tokens.items():
            if token.case_id == vault_id:
                investor_payout = token_pool_yield * (token.amount_funded_eur / vault.total_claim_amount_eur)
                print(f"     * Investor {token.investor_address[:8]}... received €{investor_payout:,.2f} dividend.")

        print("="*70 + "\n")

    def print_legal_tokenomics_summary(self):
        """Generates executive status report of tokenized legal cases and funds."""
        print("\n" + "#"*70)
        print(f"    {self.platform_name.upper()} - LEGAL TOKENOMICS & FINTECH LEDGER")
        print("#"*70)
        print(f"Total Active Case Vaults: {len(self.escrow_vaults)}")
        print(f"Total Litigation Capital Crowdfunded: €{self.total_litigation_funded_eur:,.2f}")
        print(f"Total ADR & Mediation Settlements Executed: €{self.total_adr_settled_eur:,.2f}")
        print("#"*70 + "\n")

# --- DEMONSTRAȚIE DE RULARE ---
if __name__ == "__main__":
    engine = LegalFintechTokenEngine()

    print("\n--- 1. CREARE VAULT PENTRU DOSAR DE MEDIERE/LITIGIU (RO & GERMANY JURISDICTIONS) ---")
    # Case 1: Commercial Dispute in Romania
    engine.create_case_vault("CASE-RO-2026-001", "RO_JURISDICTION", "ADR_Mediation", claim_val=100000.0, fee_percent=10.0)
    # Case 2: Cross-Border Intellectual Property Dispute in Germany
    engine.create_case_vault("CASE-DE-2026-002", "DE_JURISDICTION", "Litigation", claim_val=250000.0, fee_percent=15.0)

    print("\n--- 2. FINANȚARE TOKENIZATĂ (CROWDFUNDING PENTRU TAXE JURIDICE & MEDIERE) ---")
    engine.fund_litigation_case("0xInvestorAlpha111...", "CASE-RO-2026-001", funding_amount_eur=5000.0)
    engine.fund_litigation_case("0xInvestorBeta222...", "CASE-RO-2026-001", funding_amount_eur=10000.0)

    print("\n--- 3. DEPOZITARE DEPOZIT DE TRANZACȚIE ȘI EXECUTARE ESCROW SMART CONTRACT ---")
    engine.deposit_escrow_settlement("CASE-RO-2026-001", settlement_amount_eur=100000.0)
    engine.execute_adr_settlement_payout("CASE-RO-2026-001", local_lawyer_payout_address="0xLawyerCluj007...")

    print("\n--- 4. RAPORT GENERAL TOKENOMICS JURIDIC ---")
    engine.print_legal_tokenomics_summary()
