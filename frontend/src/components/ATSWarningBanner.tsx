/* ── ATS Warning Banner ── */

export default function ATSWarningBanner() {
    return (
        <div className="warning-banner">
            <span className="warning-banner-icon">⚠️</span>
            <span>
                ATS systems vary across platforms — results and scores are best-effort
                estimates and may differ from specific ATS implementations.
            </span>
        </div>
    );
}
