import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "SourcePixcel — Modern Online Store";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#EF4056",
          backgroundImage:
            "linear-gradient(135deg, #EF4056 0%, #d63850 100%)",
          fontFamily: "system-ui, sans-serif",
          position: "relative",
        }}
      >
        {/* Decorative circles */}
        <div
          style={{
            position: "absolute",
            top: -100,
            right: -100,
            width: 400,
            height: 400,
            borderRadius: "50%",
            background: "rgba(255, 255, 255, 0.1)",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: -150,
            left: -150,
            width: 500,
            height: 500,
            borderRadius: "50%",
            background: "rgba(255, 255, 255, 0.05)",
          }}
        />

        {/* Logo */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 20,
            marginBottom: 40,
          }}
        >
          <div
            style={{
              width: 100,
              height: 100,
              borderRadius: 24,
              background: "white",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 64,
              fontWeight: 900,
              color: "#EF4056",
            }}
          >
            S
          </div>
          <div
            style={{
              fontSize: 80,
              fontWeight: 900,
              color: "white",
              letterSpacing: -2,
            }}
          >
            SourcePixcel
          </div>
        </div>

        {/* Subtitle */}
        <div
          style={{
            fontSize: 36,
            color: "rgba(255, 255, 255, 0.9)",
            fontWeight: 500,
            textAlign: "center",
            maxWidth: 900,
          }}
        >
          فروشگاه آنلاین مدرن | Modern Online Store
        </div>

        {/* Features */}
        <div
          style={{
            display: "flex",
            gap: 30,
            marginTop: 60,
            fontSize: 24,
            color: "rgba(255, 255, 255, 0.85)",
          }}
        >
          <div>✓ ارسال سریع</div>
          <div>✓ ضمانت اصالت</div>
          <div>✓ ۷ روز بازگشت</div>
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
