// Wave-1（ZBill 裁剪）：编码套餐购买面板已下线。保留 Provider 与 hooks 的调用形状，
// 因为 MarketingTouchProvider（上游锁定文件）仍调用 useCodingPlanUpgradeDialog；
// openCodingPlanUpgrade 现为记录在案的 no-op（返回 false，不打开任何面板），
// 购买 webview、套餐清单与漏斗埋点依赖一并移除。
import { createContext, useCallback, useContext, type ReactNode } from "react";
import type { PurchaseAudience } from "@/settings/model-provider-section/codingPlanEnterpriseTiers.js";
import type { CodingPlanFunnelContext } from "@/lib/codingPlanFunnelTelemetry.js";

/** 调用形状保持与上游一致（SessionPane/Composer/Settings 传 providerId + 漏斗上下文）。 */
export interface CodingPlanUpgradeDialogTarget {
  providerId: string;
  initialAudience?: PurchaseAudience;
  initialTeamPlanKey?: string;
  funnelContext?: CodingPlanFunnelContext;
}

interface CodingPlanUpgradeDialogContextValue {
  openCodingPlanUpgrade: (
    target: CodingPlanUpgradeDialogTarget,
    observation?: { signal: AbortSignal; onResult: (opened: boolean) => void },
  ) => boolean;
}

const CodingPlanUpgradeDialogContext = createContext<CodingPlanUpgradeDialogContextValue | null>(
  null,
);

export function CodingPlanUpgradeDialogProvider({ children }: { children: ReactNode }) {
  const openCodingPlanUpgrade = useCallback(
    (
      _target: CodingPlanUpgradeDialogTarget,
      observation?: { signal: AbortSignal; onResult: (opened: boolean) => void },
    ) => {
      // ZBill 无购买面：统一入口直接拒绝；observation 的 onResult(false) 保持调用方语义完整。
      observation?.onResult(false);
      return false;
    },
    [],
  );

  return (
    <CodingPlanUpgradeDialogContext.Provider value={{ openCodingPlanUpgrade }}>
      {children}
    </CodingPlanUpgradeDialogContext.Provider>
  );
}

export function useCodingPlanUpgradeDialog() {
  const context = useContext(CodingPlanUpgradeDialogContext);
  if (!context) {
    throw new Error(
      "useCodingPlanUpgradeDialog must be used within CodingPlanUpgradeDialogProvider",
    );
  }
  return context;
}

/**
 * 可独立挂载的 conversation pane 使用可选上下文；ZBill 下打开购买面板恒为 no-op。
 */
export function useOptionalCodingPlanUpgradeDialog() {
  return useContext(CodingPlanUpgradeDialogContext);
}
