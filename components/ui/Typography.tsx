"use client";

import { cn } from "@/lib/utils";

// ═══════════════════════════════════════════════════════════════
// HEADINGS
// ═══════════════════════════════════════════════════════════════

interface HeadingProps {
  children: React.ReactNode;
  className?: string;
  as?: "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
}

export function H1({ children, className, as: Tag = "h1" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[26px] md:text-[32px] font-black leading-tight tracking-tight text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

export function H2({ children, className, as: Tag = "h2" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[20px] md:text-[24px] font-extrabold leading-snug tracking-tight text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

export function H3({ children, className, as: Tag = "h3" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[16px] md:text-[18px] font-bold leading-normal text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

export function H4({ children, className, as: Tag = "h4" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[14px] md:text-[15px] font-bold leading-normal text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

// ═══════════════════════════════════════════════════════════════
// TEXT
// ═══════════════════════════════════════════════════════════════

interface TextProps {
  children: React.ReactNode;
  className?: string;
  as?: "p" | "span" | "div";
  size?: "xs" | "sm" | "base" | "lg";
  muted?: boolean;
  weight?: "normal" | "medium" | "semibold" | "bold";
}

export function Text({
  children,
  className,
  as: Tag = "p",
  size = "base",
  muted = false,
  weight = "normal",
}: TextProps) {
  const sizes = {
    xs: "text-[11px] leading-5",
    sm: "text-[12px] leading-6",
    base: "text-[13px] leading-7",
    lg: "text-[14px] md:text-[15px] leading-8",
  };

  const weights = {
    normal: "font-normal",
    medium: "font-medium",
    semibold: "font-semibold",
    bold: "font-bold",
  };

  return (
    <Tag
      className={cn(
        sizes[size],
        weights[weight],
        muted
          ? "text-[#62666D] dark:text-[#A1A3A8]"
          : "text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

// ═══════════════════════════════════════════════════════════════
// MUTED TEXT
// ═══════════════════════════════════════════════════════════════

export function MutedText({
  children,
  className,
  size = "sm",
}: {
  children: React.ReactNode;
  className?: string;
  size?: "xs" | "sm" | "base";
}) {
  const sizes = {
    xs: "text-[10px] leading-4",
    sm: "text-[11px] leading-5",
    base: "text-[12px] leading-6",
  };

  return (
    <p
      className={cn(
        sizes[size],
        "text-[#A1A3A8] dark:text-[#6B7280]",
        className
      )}
    >
      {children}
    </p>
  );
}

// ═══════════════════════════════════════════════════════════════
// LABEL
// ═══════════════════════════════════════════════════════════════

export function Label({
  children,
  className,
  required,
}: {
  children: React.ReactNode;
  className?: string;
  required?: boolean;
}) {
  return (
    <label
      className={cn(
        "block text-[12px] font-medium text-[#62666D] dark:text-[#A1A3A8] mb-1.5",
        className
      )}
    >
      {children}
      {required && <span className="text-[#EF4056] ml-1">*</span>}
    </label>
  );
}

// ═══════════════════════════════════════════════════════════════
// PRICE TEXT
// ═══════════════════════════════════════════════════════════════

export function PriceText({
  children,
  className,
  size = "base",
  discount,
}: {
  children: React.ReactNode;
  className?: string;
  size?: "sm" | "base" | "lg" | "xl";
  discount?: boolean;
}) {
  const sizes = {
    sm: "text-[13px]",
    base: "text-[15px]",
    lg: "text-[18px]",
    xl: "text-[24px]",
  };

  return (
    <span
      className={cn(
        sizes[size],
        "font-bold tabular-nums",
        discount
          ? "text-[#EF4056]"
          : "text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </span>
  );
}

// ═══════════════════════════════════════════════════════════════
// DIVIDER
// ═══════════════════════════════════════════════════════════════

export function Divider({
  className,
  spacing = "md",
}: {
  className?: string;
  spacing?: "sm" | "md" | "lg";
}) {
  const spacings = {
    sm: "my-3",
    md: "my-4",
    lg: "my-6",
  };

  return (
    <div
      className={cn(
        "border-t border-[#E0E0E2] dark:border-[#2A2A2E]",
        spacings[spacing],
        className
      )}
    />
  );
}

// ═══════════════════════════════════════════════════════════════
// SECTION
// ═══════════════════════════════════════════════════════════════

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  spacing?: "sm" | "md" | "lg";
}

export function Section({
  children,
  className,
  spacing = "md",
}: SectionProps) {
  const spacings = {
    sm: "space-y-3",
    md: "space-y-4",
    lg: "space-y-6",
  };

  return <div className={cn(spacings[spacing], className)}>{children}</div>;
}

// ═══════════════════════════════════════════════════════════════
// CONTAINER
// ═══════════════════════════════════════════════════════════════

export function Container({
  children,
  className,
  size = "default",
}: {
  children: React.ReactNode;
  className?: string;
  size?: "default" | "narrow" | "wide";
}) {
  const sizes = {
    narrow: "max-w-3xl",
    default: "max-w-[1400px]",
    wide: "max-w-[1600px]",
  };

  return (
    <div className={cn("mx-auto px-4 md:px-6", sizes[size], className)}>
      {children}
    </div>
  );
}
