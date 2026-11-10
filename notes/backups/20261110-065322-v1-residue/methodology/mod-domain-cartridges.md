# MOD-DOMAIN-CARTRIDGES — Registry Domain Web3 (plug-and-play)

Plug-in METHODOLOGY-SEGITIGA tahap B (peta siklus) & C (invarian senyap).
**Kontrak ekstensi**: domain baru = append satu blok di bawah; core tidak disentuh.

Format blok: Domain | Siklus aliran (L-PATH) | Invarian senyap | Cartridge POV | Catatan off-chain.

---

### BRIDGE (cross-chain intents)
- **Siklus**: deposit → fill → worker bundle → propose(bond) → jendela dispute → execute →
  relay roots → refund leaf → bridge-back.
- **Invarian senyap**: "leaf tak pernah membayar melebihi pot"; "msg.value dipakai ATAU dikembalikan";
  "slot root identik antar-chain adalah desain"; "handler selalu kosong di antara fill"
  (invarian generik bridge — verifikasi ulang terhadap desain protokol yang diaudit).
- **POV**: M-009 (in-flight), POV-TON-01 (async), POV-CALL-02; kelas transient-holder (MulticallHandler).
- **Off-chain**: data worker (bundle), disputer (jendela 2 jam — kelas "ketiadaan aksi"), relayer (pricing).

### LENDING (borrow/lend/collateral)
- **Siklus**: supply → borrow → oracle update → liquidate → auction/bad-debt → repay → withdraw.
- **Invarian senyap**: "kolateral tak pernah < utang tanpa likuidasi tersedia"; "oracle tak bisa
  di-flashloan"; "share/debt tak bocor oleh pembulatan"; "bad debt tak tersosialisasi murah".
- **POV**: POV-DEFI-01 (self-liquidation, bad-debt socialization), POV-DEFI-02 (valuation vs execution), M-007.
- **Off-chain**: keeper likuidasi (diam = kelas ketiadaan-aksi), oracle relayer.

### LP / AMM
- **Siklus**: addLiquidity → swap → fee accrual → arb balik → removeLiquidity; flashloan loop.
- **Invarian senyap**: "k konstan (xy=k)"; "fee monoton, non-decreasing"; "callback token tidak
  reenter di state timpang"; "LP token mint/burn persis proporsional".
- **POV**: POV-MATH-02 (inverse rounding), POV-CALL-01, M-007 (salami), M-003 (flashloan identitas ganda).
- **Off-chain**: bot arbitrase, quoter (harga off-chain vs pool on-chain = AF-09).

### STAKING / REWARDS
- **Siklus**: stake → accrual (indeks) → claim → unstake(cooldown) → withdraw.
- **Invarian senyap**: "indeks akrual tak bisa di-smear sebelum stake"; "cooldown window tak bisa
  di-bypass"; "reward claim idempoten".
- **POV**: POV-MATH-01 (indeks akrual desync), M-009 (cooldown = half-baked), M-007.
- **Off-chain**: validator/orchestrator reward computation.

### NFT (escrow/auction/royalty/staking)
- **Siklus**: mint → list → bid → settle → royalty → stake → claim reward.
- **Invarian senyap**: "royalty tak bisa di-bypass di jalur samping"; "finalitas lelang (bid akhir
  tidak di-revert oleh race)"; "tokenId unik tak tertukar".
- **POV**: M-009 (jendela bid), M-006 Prinsip B ([A,A] tokenId), POV-CALL-01 (onERC721Received).
- **Catatan jujur**: segitiga menutup PLUMBING FINANSIAL NFT; nilai subjektif (rarity/metadata)
  off-chain TIDAK terjangkau census — untuk NFT murni, metode merosot jadi code-first.

### DERIVATIF / OPTIONS / PERPS
- **Siklus**: open → margin → oracle settle → PnL → exercise/expiry window → liquidation.
- **Invarian senyap**: "exercise window = race window"; "PnL settle membaca harga SATU kali";
  "margin tak negatif tanpa likuidasi".
- **POV**: POV-DEFI-02, M-009, M-002 (PnL delta), AF-08 (temporal).
- **Off-chain**: oracle relayer, settlement keeper.

---

## Cara menambah domain baru (blok template)

```markdown
### <DOMAIN>
- **Siklus**: <hop1> → <hop2> → ... (node kontrak, edge aliran)
- **Invarian senyap**: <asumsi yang TIDAK di-assert — target serangan>
- **POV**: <cartridge dari ref-pov-*.md yang relevan>
- **Off-chain**: <aktor luar + kelas ketiadaan-aksi bila ada>
```
