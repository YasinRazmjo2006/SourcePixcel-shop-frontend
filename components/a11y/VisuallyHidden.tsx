interface VisuallyHiddenProps {
  children: React.ReactNode;
  as?: "span" | "div";
}

/**
 * VisuallyHidden — hides content visually but keeps it for screen readers.
 */
export default function VisuallyHidden({
  children,
  as: Tag = "span",
}: VisuallyHiddenProps) {
  return (
    <Tag className="sr-only">
      {children}
    </Tag>
  );
}
