Shader "Vertex Color" {
 SubShader {
    Tags { "RenderType" = "Opaque" }

    CGPROGRAM
    #pragma surface surf Lambert

    struct Input {
        float4 color : COLOR;
    };

    void surf (Input IN, inout SurfaceOutput o) {
        o.Albedo = IN.color;
    }

    ENDCG
  }

  Fallback "Diffuse"
}
