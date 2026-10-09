import { Check } from "lucide-react";
import type { Locale } from "@/lib/types";

interface StepIndicatorProps {
  currentStep: number;
  steps: { fa: string; en: string }[];
  locale: Locale;
}

export default function StepIndicator({
  currentStep,
  steps,
  locale,
}: StepIndicatorProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 mb-4">
      <div className="flex items-center justify-between max-w-2xl mx-auto">
        {steps.map((step, i) => {
          const stepNum = i + 1;
          const isActive = stepNum === currentStep;
          const isDone = stepNum < currentStep;

          return (
            <div key={i} className="flex items-center flex-1">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-[12px] font-bold transition-colors ${
                    isDone
                      ? "bg-[#22C55E] text-white"
                      : isActive
                      ? "bg-[#EF4056] text-white"
                      : "bg-[#F5F5F5] text-[#A1A3A8]"
                  }`}
                >
                  {isDone ? (
                    <Check size={14} />
                  ) : isFa ? (
                    stepNum.toLocaleString("fa-IR")
                  ) : (
                    stepNum
                  )}
                </div>
                <span
                  className={`text-[11px] text-center whitespace-nowrap ${
                    isActive
                      ? "text-[#EF4056] font-medium"
                      : isDone
                      ? "text-[#22C55E]"
                      : "text-[#A1A3A8]"
                  }`}
                >
                  {isFa ? step.fa : step.en}
                </span>
              </div>

              {i < steps.length - 1 && (
                <div
                  className={`flex-1 h-[2px] mx-2 mb-6 transition-colors ${
                    isDone ? "bg-[#22C55E]" : "bg-[#E0E0E2]"
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
