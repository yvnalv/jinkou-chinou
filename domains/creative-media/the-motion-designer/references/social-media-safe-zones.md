# Social Media Platform Formats & UI Overlay Safe Zones

When a video plays on Instagram, TikTok, YouTube, LinkedIn, Facebook, or X, the platform overlays native UI controls (profile handles, expandable captions, Like/Comment/Repost/Share icon stacks, audio tickers, and progress bars) directly on top of the video canvas.

Every composition created by `the-motion-designer` must select a **Platform Preset** first and strictly keep **all titles, logos, key UI mockups, and Closed Captions (CC)** inside that platform's safe zone.

---

## 1. Complete Platform & Placement Format Matrix

| Platform | Placement Type | Aspect Ratio | Canvas (`W × H` px) | Recommended FPS | Duration Sweet Spot (Max Limit) |
|---|---|---:|---:|---:|---|
| **Instagram** | **Reels** *(Full-Screen + 4:5 Feed Crop)* | `9:16` | `1080 × 1920` | `30` or `60` | `7s–90s` (up to 15m) |
| **Instagram** | **Stories** | `9:16` | `1080 × 1920` | `30` or `60` | `15s–60s` |
| **Instagram** | **Feed Portrait** *(Highest Feed Reach)* | `4:5` | `1080 × 1350` | `30` or `60` | `15s–60s` (up to 60m) |
| **Instagram** | **Feed Square** | `1:1` | `1080 × 1080` | `30` | `15s–60s` |
| **TikTok** | **In-Feed / Organic / Spark Ad** | `9:16` | `1080 × 1920` | `30` or `60` | `15s–60s` (up to 10m) |
| **YouTube** | **YouTube Shorts** *(Vertical)* | `9:16` | `1080 × 1920` | `30` or `60` | `15s–60s` (up to 3m) |
| **YouTube** | **Standard HD / 4K** *(Landscape)* | `16:9` | `1920 × 1080` / `3840 × 2160` | `30` or `60` | `30s–12h` |
| **LinkedIn** | **Feed Portrait** *(Mobile-First)* | `4:5` | `1080 × 1350` | `30` | `15s–90s` (up to 10m) |
| **LinkedIn** | **Feed Square** | `1:1` | `1080 × 1080` | `30` | `15s–90s` |
| **LinkedIn** | **Vertical Video** | `9:16` | `1080 × 1920` | `30` | `15s–3m` |
| **LinkedIn** | **Desktop B2B Landscape** | `16:9` | `1920 × 1080` | `30` or `60` | `30s–3m` |
| **Facebook** | **Facebook Reels / Stories** | `9:16` | `1080 × 1920` | `30` or `60` | `15s–90s` |
| **Facebook** | **Feed Portrait / Square** | `4:5` / `1:1` | `1080 × 1350` / `1080 × 1080` | `30` | `15s–3m` |
| **X (Twitter)** | **Landscape Product Demo** | `16:9` | `1920 × 1080` | `30` or `60` | `15s–140s` |
| **X (Twitter)** | **Square / Vertical Feed** | `1:1` / `9:16` | `1080 × 1080` / `1080 × 1920` | `30` | `15s–140s` |
| **Universal** | **Cross-Platform Short-Form Master** | `9:16` | `1080 × 1920` | `30` or `60` | `15s–60s` *(Fits IG + TikTok + Shorts + FB)* |
| **Web / Deck** | **Website Hero / Docs Loop / Slide** | `16:9` / Custom | `1920 × 1080` or Custom | `30` or `60` | Any |

---

## 2. Visual Map of `9:16` (`1080 × 1920`) Center-Locked Safe Stage & Fixed Header

> **Critical Center-Lock Rule**: Never use asymmetric left/right container margins (like `left: 60, right: 192`) for your main content container—that shifts the visual center to `X = 474px` and makes the layout look off-center! Instead, use **symmetric horizontal margins (`left = 160px, right = 160px`, width `760px`, center `X = 540px`)** so the main content and Closed Captions are **100% horizontally and vertically centered** while clearing the right-side UI button stack.

```text
+--------------------------------------------------+  Y = 0 px
|  [TOP UI DEAD ZONE: Y = 0 to 288 px]             |
|  - OS Status Bar, Notch / Dynamic Island         |
|  - IG 4:5 Home Feed Top Crop (Y = 285 px)        |
+--------------------------------------------------+  Y = 288 px
|        [FIXED TOP HEADER: Y = 288..344 px]       |
|        [Logo: Top-Left]        [Icon: Top-Right] |
|        (X = 160 px)                 (X = 920 px) |
|  +------------------------------------+          |  Y = 360 px
|  |                                    |  RIGHT   |
|  |   CENTER-LOCKED MAIN CONTENT       |  UI      |
|  |   CONTAINER (X: 160 to 920 px)     |  ACTION  |
|  |   (Width: 760 px, Center: X=540)   |  STACK   |
|  |   (Y: 360 to 1060 px, Centered)    |  DEAD    |
|  |                                    |  ZONE    |
|  |   Vertically & Horizontally        |  (X: 920 |
|  |   Centered Cards, Charts & Copy    |  to 1080)|
|  +------------------------------------+  Like    |  Y = 1060 px
|  +------------------------------------+  Comment |  Y = 1080 px
|  |   CENTERED CLOSED CAPTIONS (CC)    |  Repost  |
|  |   (X: 160..920 px, Y: 1080..1220)  |  Save    |
|  +------------------------------------+  Share   |  Y = 1220 px
+--------------------------------------------------+  Y = 1248 px (Bottom of IG 4:5 Feed Crop)
|  [BOTTOM UI DEAD ZONE: Y = 1248..1920]           |
|  - @username + Follow / Subscribe pill           |
|  - 2–4 lines of expandable post caption          |
|  - Scrolling audio marquee + progress scrubber   |
+--------------------------------------------------+  Y = 1920 px
X = 0    X = 160                        X = 920    X = 1080 px
```

---

## 3. Exact Pixel Safe-Zone Table by Platform Preset

All measurements are in pixels relative to the target canvas (`top`, `bottom`, `left`, `right` dead-zone insets, plus the recommended `ccBand` Y-range for subtitles/closed captions):

| Preset ID | Canvas (`W × H`) | Top Inset | Bottom Inset | Left Inset | Right Inset | Safe Content Box (`W × H`) | Subtitle / CC Safe Y-Band | What Blocks the Edges? |
|---|---|---|---|---|---|---|---|---|
| `instagram-reels` | `1080 × 1920` | `285 px` | `672 px` | `60 px` | `120 px` | `900 × 963 px` | `Y: 1050–1220 px` | Top camera/Reels header; right Like/Comment/Repost/Save/Audio column; bottom `@handle`, caption, audio pill; **plus `4:5` Home Feed crop cuts `285px` top & bottom** (`Y: 285..1635`). |
| `instagram-stories` | `1080 × 1920` | `250 px` | `340 px` | `60 px` | `60 px` | `960 × 1330 px` | `Y: 1360–1520 px` | Top Story progress bars, profile badge, close button; bottom "Send message" input bar, Like heart, Share plane. |
| `tiktok` | `1080 × 1920` | `240 px` | `660 px` | `60 px` | `180 px` | `840 × 1020 px` | `Y: 1040–1210 px` | Top "Following / For You / Shop" tabs & search; right 180px column (from `Y=840` down: creator avatar, Heart, Comment, Bookmark, Share, spinning record); bottom handle, 4-line caption, sound ticker. |
| `youtube-shorts` | `1080 × 1920` | `288 px` | `672 px` | `48 px` | `192 px` | `840 × 960 px` | `Y: 1040–1200 px` | Top Search/Camera/Menu; right 192px column (Like, Dislike, Comment, Share, Remix, Audio thumb); bottom Channel avatar, `@handle`, Subscribe button, multi-line title, red progress bar. |
| `facebook-reels` | `1080 × 1920` | `260 px` | `650 px` | `60 px` | `160 px` | `860 × 1010 px` | `Y: 1050–1220 px` | Top Reels header & profile menu; right Like/Comment/Share/More stack; bottom username, Follow link, caption, audio track, and Stars/CTA button. |
| `universal-vertical` | `1080 × 1920` | **`288 px`** | **`672 px`** | **`60 px`** | **`192 px`** | **`828 × 960 px`** | **`Y: 1040–1200 px`** | **Strictest intersection of IG Reels (including 4:5 crop), TikTok, YouTube Shorts, and FB Reels.** Use this when exporting one master `9:16` file for all platforms. |
| `feed-portrait-4-5` | `1080 × 1350` | `90 px` | `160 px` | `60 px` | `90 px` | `930 × 1100 px` | `Y: 1020–1160 px` | Bottom-right mute/unmute pill, bottom-left product tag pill, carousel pagination dots, and video scrubber bar. |
| `feed-square-1-1` | `1080 × 1080` | `80 px` | `140 px` | `60 px` | `80 px` | `940 × 860 px` | `Y: 810–920 px` | Bottom mute/unmute icon, timestamp pill, and hover playback controls on Instagram, LinkedIn, and X. |
| `youtube-16-9` | `1920 × 1080` | `90 px` | `160 px` | `120 px` | `120 px` | `1680 × 830 px` | `Y: 790–900 px` | Bottom timeline scrubber, play/volume/settings bar, chapter title, and bottom-right channel watermark (`150×150px`); top-right info cards. |
| `web-clean` | `1920 × 1080` | `60 px` | `80 px` | `80 px` | `80 px` | `1760 × 940 px` | `Y: 860–970 px` | Standard title-safe margin (5%–7%) for website hero embeds, pitch decks, and documentation GIFs. |

---

## 4. Rules for Center-Locked Layout, Fixed Header & Closed Captions (CC)

1. **Always Center the Main Content Container Horizontally and Vertically**:
   * Never apply asymmetric left/right container bounds (such as `left: 60px, right: 192px`) to the main content stage, as that shifts the layout off-center.
   * Instead, use **symmetric horizontal margins (`left = right = max(leftDeadZone, rightDeadZone)`)**, such as `left: 160px, right: 160px` (`width: 760px`, centered at `X = 540px` on `1080×1920`), and center the main stage container both horizontally and vertically (`display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'`).
2. **Fixed Top-Left Logo & Top-Right Icon/Status Header**:
   * Place a persistent top header row anchored at the top of the safe zone (`top: 288px` on `9:16`, `left: 160px`, `right: 160px`, `display: 'flex', justifyContent: 'space-between', alignItems: 'center'`):
     * **Top-Left**: Brand logo or wordmark in a fixed position.
     * **Top-Right**: Geometric `<svg>` icon or compact scene indicator (`01 / 04`) in a fixed position.
3. **Horizontally Centered Subtitles / Closed Captions (CC)**:
   * On `9:16` mobile feeds (Instagram Reels, TikTok, Shorts), the bottom **35% (`Y = 1248 to 1920 px`)** is covered by the post caption, username, and audio ticker.
   * Place `9:16` subtitles inside **`Y = 1080 to 1220 px`** and horizontally centered on the canvas (`left: 160px, right: 160px, width: 760px, display: 'flex', justifyContent: 'center'`).
4. **Solid High-Contrast Readability Pill**:
   * Give subtitles a solid dark/light surface pill (`#111827` with a `1px` or `2px` solid border `#1E293B`, `borderRadius: 12`, `padding: '12px 24px'`) so captions remain crisp and legible.
5. **Always Include `<SafeZoneOverlay />` in Studio Preview**:
   * Render `<SafeZoneOverlay platform={platform} enabled={showSafeZoneGuide} />` as the top-most layer in your composition (`assets/SafeZoneOverlay.starter.tsx`).

