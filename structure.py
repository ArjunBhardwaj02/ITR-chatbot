# %%
from pydantic import BaseModel , Field
from typing import Optional, Literal, List

# %%
# This is the lowest level. It represents a single row in the tax bracket table.
class TaxSlab(BaseModel):
    min_Income : int = Field(description="The starting point of the slab (e.g., 0, 400000)")
    max_Income : Optional[int] = Field(default=None, description="The Endpoint of the tax slab")
    tax_rate_percentage: float = Field(description="The actual tax percentage for that bracket.")

# %%
# This is the middle layer. It groups the individual slabs together and holds the rules specific to that overarching regime.
class TaxRegime(BaseModel):
    regime_name : Literal["New","Old"] = Field(description="'New' for section 202(1) default regime, 'Old' for the opt-out regime where deductions like 80C apply.")
    tax_year: str = Field(description="To capture the year, aligning with the new terminology in the 2025 Act")
    standard_deduction: Optional[int] = Field(default=None,description="The default deduction amount")
    rebate_limit_87a : Optional[int] = Field(default=None,description="The maximum income limit upto which total tax drop to zero")
    slabs: List[TaxSlab] = Field(description="To nest the previous model so the LLM extract an organized array of brackets rules")
    rebate_amount_87a: Optional[int] = Field(
        default=None,
        description="Maximum rebate amount under section 87A in INR (New: 60000, Old: 12500)"
    )
    basic_exemption_limit: Optional[int] = Field(
        default=None,
        description="Basic exemption below which no tax is payable (New: 400000, Old: 250000 for FY 2026-27)"
    )

# %%
class AllowancesAndExemptions(BaseModel):
    allowance_name: str = Field(description="Name e.g. 'HRA', 'Children Education Allowance', 'LTA'")
    section_reference: str = Field(
        description="Relevant section in Income-tax Act 2025 e.g. 'Section 10(13A)'"
    )
    category: Literal["Allowance", "Perquisite", "Deduction", "Exemption"] = Field(
        description="Type of tax benefit"
    )
    monthly_limit_per_person: Optional[int] = Field(
        default=None,
        description="Monthly cap in INR if applicable"
    )
    annual_limit: Optional[int] = Field(
        default=None,
        description="Annual cap in INR if applicable (e.g. LTA: actual fare, 80C: 150000)"
    )
    is_applicable_new_regime: bool = Field(
        description="True if this benefit is available under the New regime"
    )
    is_applicable_old_regime: bool = Field(
        default=True,
        description="True if available under Old regime (most are)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Conditions, exceptions, or computation method e.g. 'Least of actual HRA, 50%/40% of salary, rent minus 10% salary'"
    )

# %%
class DeductionSection(BaseModel):
    section: str = Field(description="Section number e.g. '80C', '80D', '80CCD(1B)'")
    description: str = Field(description="What the deduction is for")
    max_deduction: Optional[int] = Field(description="Annual cap in INR e.g. 150000 for 80C")
    is_applicable_new_regime: bool = Field(description="80C, 80D etc. are NOT available in new regime")
    eligible_investments: Optional[List[str]] = Field(
        default=None,
        description="List of qualifying instruments e.g. ['PPF', 'ELSS', 'NSC', 'Life Insurance Premium']"
    )

# %%
class TaxDocumentExtraction(BaseModel):
    regimes: List[TaxRegime] = Field(description="Extracted tax regimes and their slabs")
    allowances: List[AllowancesAndExemptions] = Field(description="Extracted allowances")
    deductions: List[DeductionSection] = Field(description="Extracted deductions under Chapter VI-A")

# %%


# %%



