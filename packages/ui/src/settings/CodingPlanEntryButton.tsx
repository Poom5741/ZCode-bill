import type { ComponentProps } from "react";
import { Button } from "@/components/ui/button.js";

// Wave-1（ZBill 裁剪）：购买入口闸门（套餐清单查询）已下线；闸门恒为 ready，
// CodingPlanEntryButton 退化为普通按钮。调用方（配额横幅/侧栏用量等）保持编译与交互完整。
// 返回类型保留三态联合，调用方的 loading/error 分支无需同步改动。
export function useCodingPlanEntryGate(): {
  status: "ready" | "loading" | "error";
  label: string | undefined;
  retry: (() => void) | undefined;
} {
  return { status: "ready", label: undefined, retry: undefined };
}

/** 各入口共享同一查询状态；失败时按钮只重试，不继续执行购买动作。 */
export function CodingPlanEntryButton({
  children,
  disabled,
  onClick,
  bypassGate = false,
  ...props
}: ComponentProps<typeof Button> & { bypassGate?: boolean }) {
  const gate = useCodingPlanEntryGate();
  const status = bypassGate ? "ready" : gate.status;
  return (
    <Button
      {...props}
      disabled={disabled || status === "loading"}
      aria-label={status === "ready" ? props["aria-label"] : gate.label}
      aria-busy={status === "loading"}
      title={status === "ready" ? props.title : gate.label}
      onClick={(event) => {
        if (status === "error") {
          event.preventDefault();
          event.stopPropagation();
          gate.retry?.();
          return;
        }
        if (status === "ready") onClick?.(event);
      }}
    >
      {status === "ready" ? children : gate.label}
    </Button>
  );
}
