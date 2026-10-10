import type { Variants, Transition } from "framer-motion";

// ═══════════════════════════════════════════════════════════════
// TRANSITIONS
// ═══════════════════════════════════════════════════════════════

export const spring: Transition = {
  type: "spring",
  stiffness: 300,
  damping: 30,
};

export const springSoft: Transition = {
  type: "spring",
  stiffness: 200,
  damping: 25,
};

export const easeOut: Transition = {
  duration: 0.3,
  ease: [0.16, 1, 0.3, 1],
};

export const easeInOut: Transition = {
  duration: 0.4,
  ease: [0.65, 0, 0.35, 1],
};

export const smooth: Transition = {
  duration: 0.5,
  ease: [0.22, 1, 0.36, 1],
};

// ═══════════════════════════════════════════════════════════════
// PAGE TRANSITIONS
// ═══════════════════════════════════════════════════════════════

export const pageVariants: Variants = {
  initial: {
    opacity: 0,
    y: 8,
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: [0.16, 1, 0.3, 1],
    },
  },
  exit: {
    opacity: 0,
    y: -8,
    transition: {
      duration: 0.2,
      ease: [0.65, 0, 0.35, 1],
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// FADE
// ═══════════════════════════════════════════════════════════════

export const fadeInVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.3 },
  },
};

// ═══════════════════════════════════════════════════════════════
// SLIDE UP (for sections)
// ═══════════════════════════════════════════════════════════════

export const slideUpVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 24,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: [0.22, 1, 0.36, 1],
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// SCALE IN (for modals, dropdowns)
// ═══════════════════════════════════════════════════════════════

export const scaleInVariants: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.95,
  },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.2,
      ease: [0.16, 1, 0.3, 1],
    },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: {
      duration: 0.15,
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// STAGGER (for lists)
// ═══════════════════════════════════════════════════════════════

export const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.05,
    },
  },
};

export const itemVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 12,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.35,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// HOVER EFFECTS
// ═══════════════════════════════════════════════════════════════

export const cardHoverVariants: Variants = {
  rest: {
    y: 0,
    boxShadow: "0 2px 8px -2px rgb(0 0 0 / 0.06)",
  },
  hover: {
    y: -4,
    boxShadow: "0 12px 32px -8px rgb(0 0 0 / 0.12)",
    transition: {
      duration: 0.25,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

export const buttonTapVariants = {
  rest: { scale: 1 },
  hover: { scale: 1.02 },
  tap: { scale: 0.97 },
};

// ═══════════════════════════════════════════════════════════════
// DRAWER (mobile menu, filters)
// ═══════════════════════════════════════════════════════════════

export const drawerVariants = (isFa: boolean): Variants => ({
  hidden: {
    x: isFa ? "100%" : "-100%",
    opacity: 0,
  },
  visible: {
    x: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30,
    },
  },
  exit: {
    x: isFa ? "100%" : "-100%",
    opacity: 0,
    transition: {
      duration: 0.2,
    },
  },
});

export const backdropVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};

// ═══════════════════════════════════════════════════════════════
// SLIDER (carousel)
// ═══════════════════════════════════════════════════════════════

export const slideVariants: Variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? "100%" : "-100%",
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
    transition: {
      duration: 0.4,
      ease: [0.22, 1, 0.36, 1],
    },
  },
  exit: (direction: number) => ({
    x: direction > 0 ? "-100%" : "100%",
    opacity: 0,
    transition: {
      duration: 0.3,
      ease: [0.65, 0, 0.35, 1],
    },
  }),
};
