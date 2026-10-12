"use client";

import { useCallback, useRef, useState, useEffect } from "react";

export function useVirtualRows(
  rowCount: number,
  rowHeight: number,
  containerHeight: number,
  overscan = 5
) {
  const [scrollTop, setScrollTop] = useState(0);

  const startIndex = Math.max(0, Math.floor(scrollTop / rowHeight) - overscan);
  const endIndex = Math.min(
    rowCount - 1,
    Math.floor((scrollTop + containerHeight) / rowHeight) + overscan
  );

  const totalHeight = rowCount * rowHeight;

  const handleScroll = useCallback((e: React.UIEvent<HTMLElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);

  return {
    startIndex,
    endIndex,
    totalHeight,
    handleScroll,
    offsetY: startIndex * rowHeight,
  };
}
