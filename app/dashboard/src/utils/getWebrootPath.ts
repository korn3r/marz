export function getWebrootPath(): string {
    const staticUrl = Array.from(
        document.querySelectorAll<HTMLScriptElement | HTMLLinkElement>(
            'script[src], link[href]'
        )
    )
        .map((element) => element.getAttribute("src") || element.getAttribute("href") || "")
        .find((url) => url.includes("/statics/"));

    if (!staticUrl) {
        return "";
    }

    const pathname = new URL(staticUrl, window.location.origin).pathname;
    const staticsIndex = pathname.indexOf("/statics/");

    if (staticsIndex === -1) {
        return "";
    }

    return pathname.slice(0, staticsIndex);
}
