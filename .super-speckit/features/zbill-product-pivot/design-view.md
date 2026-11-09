# Design view — zbill-product-pivot (Mermaid fallback)

Source: [design-view.mmd](design-view.mmd)

```mermaid
flowchart LR
  Owner[Owner: confirmed scope answers 2026-11-09] --> Purpose[Purpose gate: ZBill pivot]
  Purpose --> W1[Wave 1: delete purchase / marketplace / automations]
  Purpose --> W2[Wave 2: delete remote connections / remote control]
  Purpose --> W3[Wave 3: bill features]
  subgraph Kept[Agent core kept]
    Chat[Chat main view] --> Agent[Session runtime + host RPC]
    Files[File tree panel] --> Agent
    Doc[Document panel] --> Report[(Report files xlsx+PDF)]
    Provider[Provider connection config] --> Agent
    Skills[skillsService discoverSkills] --> Agent
  end
  W1 --> Kept
  W2 --> Kept
  W3 --> Pipeline[zbill-billing pipeline]
  Pipeline --> Report
  Review[Item review/edit UI] --> Items[(items.json overrides)]
  Items --> Pipeline
  Archive[Archive index store: single owner] --> Doc
```

Limitation: Archify renderer is not installed in this environment; this is a Mermaid
fallback with the same factual content and source links. It is a shared explanation, not
product proof — repo checks and public-behavior verification enforce the actual contract.
