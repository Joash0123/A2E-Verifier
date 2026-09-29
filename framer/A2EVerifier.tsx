import * as React from "react"

type Action = {
    tool: string
    operation: string
    resource: string
    parameters: Record<string, any>
    context: Record<string, any>
    actor: string
}

type Result = {
    allowed: boolean
    verdict: string
    authorized: Action
    executed: Action
    investigation?: {
        summary: string
        category: string
        evidence: string[]
        remediation: string[]
    }
}

export default function A2EVerifier() {
    const [authorized, setAuthorized] = React.useState<Action>({
        tool: "",
        operation: "",
        resource: "",
        parameters: {},
        context: {},
        actor: "",
    })

    const [executed, setExecuted] = React.useState<Action>({
        tool: "",
        operation: "",
        resource: "",
        parameters: {},
        context: {},
        actor: "",
    })

    const [result, setResult] = React.useState<Result | null>(null)
    const [loading, setLoading] = React.useState(false)
    const [error, setError] = React.useState("")

    const update = (
        type: "authorized" | "executed",
        field: keyof Action,
        value: string
    ) => {
        if (type === "authorized") {
            setAuthorized(prev => ({ ...prev, [field]: value }))
        } else {
            setExecuted(prev => ({ ...prev, [field]: value }))
        }
    }

    const verify = async () => {
        setLoading(true)
        setError("")
        setResult(null)

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/verify",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "*/*"
                    },
                    body: JSON.stringify({
                        authorized,
                        executed
                    })
                }
            )

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`)
            }

            const data = await response.json()
            setResult(data)
        } catch (error) {
            setError(
                "Unable to connect to the A2E-Verifier API. Make sure FastAPI is running on port 8000."
            )
        } finally {
            setLoading(false)
        }
    }

    const inputStyle: React.CSSProperties = {
        width: "100%",
        boxSizing: "border-box",
        padding: "10px",
        borderRadius: "8px",
        border: "1px solid #303030",
        background: "#111",
        color: "#fff",
        fontSize: "13px"
    }

    const field = (
        label: string,
        type: "authorized" | "executed",
        name: keyof Action
    ) => {
        const value =
            type === "authorized"
                ? authorized[name]
                : executed[name]

        return (
            <div style={{ marginBottom: "12px" }}>
                <div
                    style={{
                        fontSize: "10px",
                        color: "#888",
                        marginBottom: "5px",
                        textTransform: "uppercase",
                        letterSpacing: "0.8px"
                    }}
                >
                    {label}
                </div>

                <input
                    style={inputStyle}
                    value={
                        typeof value === "string"
                            ? value
                            : JSON.stringify(value)
                    }
                    onChange={e =>
                        update(type, name, e.target.value)
                    }
                />
            </div>
        )
    }

    return (
        <div
            style={{
                width: "100%",
                minHeight: "100%",
                padding: "24px",
                boxSizing: "border-box",
                background: "#050505",
                color: "#fff",
                fontFamily:
                    "Inter, system-ui, -apple-system, sans-serif"
            }}
        >
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fit, minmax(280px, 1fr))",
                    gap: "16px"
                }}
            >
                <div
                    style={{
                        padding: "20px",
                        borderRadius: "14px",
                        border: "1px solid #252525",
                        background: "#0b0b0b"
                    }}
                >
                    <div
                        style={{
                            fontSize: "12px",
                            fontWeight: 700,
                            letterSpacing: "1px",
                            marginBottom: "18px"
                        }}
                    >
                        AUTHORIZED ACTION
                    </div>

                    {field("Tool", "authorized", "tool")}
                    {field("Operation", "authorized", "operation")}
                    {field("Resource", "authorized", "resource")}
                    {field("Actor", "authorized", "actor")}
                </div>

                <div
                    style={{
                        padding: "20px",
                        borderRadius: "14px",
                        border: "1px solid #252525",
                        background: "#0b0b0b"
                    }}
                >
                    <div
                        style={{
                            fontSize: "12px",
                            fontWeight: 700,
                            letterSpacing: "1px",
                            marginBottom: "18px"
                        }}
                    >
                        EXECUTED ACTION
                    </div>

                    {field("Tool", "executed", "tool")}
                    {field("Operation", "executed", "operation")}
                    {field("Resource", "executed", "resource")}
                    {field("Actor", "executed", "actor")}
                </div>
            </div>

            <button
                onClick={verify}
                disabled={loading}
                style={{
                    width: "100%",
                    marginTop: "18px",
                    padding: "14px",
                    borderRadius: "10px",
                    border: "none",
                    background: "#fff",
                    color: "#000",
                    fontWeight: 700,
                    cursor: loading ? "wait" : "pointer"
                }}
            >
                {loading
                    ? "VERIFYING..."
                    : "RUN VERIFICATION"}
            </button>

            {error && (
                <div
                    style={{
                        marginTop: "16px",
                        padding: "16px",
                        borderRadius: "10px",
                        background: "#160909",
                        border: "1px solid #552222",
                        color: "#ff7b7b"
                    }}
                >
                    {error}
                </div>
            )}

            {result && (
                <div
                    style={{
                        marginTop: "18px",
                        padding: "20px",
                        borderRadius: "14px",
                        border: "1px solid #252525",
                        background: "#0b0b0b"
                    }}
                >
                    <div
                        style={{
                            fontSize: "10px",
                            color: "#888",
                            letterSpacing: "1px"
                        }}
                    >
                        VERIFICATION RESULT
                    </div>

                    <div
                        style={{
                            fontSize: "28px",
                            fontWeight: 800,
                            marginTop: "8px"
                        }}
                    >
                        {result.allowed ? "✓" : "✕"}{" "}
                        {result.verdict}
                    </div>

                    {result.investigation && (
                        <>
                            <div
                                style={{
                                    marginTop: "12px",
                                    color: "#ccc",
                                    fontSize: "14px"
                                }}
                            >
                                {result.investigation.summary}
                            </div>

                            <div
                                style={{
                                    marginTop: "16px",
                                    fontSize: "12px",
                                    color: "#aaa"
                                }}
                            >
                                CATEGORY
                            </div>

                            <div style={{ marginTop: "5px" }}>
                                {result.investigation.category}
                            </div>

                            <div
                                style={{
                                    marginTop: "16px",
                                    fontSize: "12px",
                                    color: "#aaa"
                                }}
                            >
                                EVIDENCE
                            </div>

                            <div style={{ marginTop: "8px" }}>
                                {result.investigation.evidence.map(
                                    (item, index) => (
                                        <div
                                            key={index}
                                            style={{
                                                marginBottom: "6px",
                                                color: "#ccc",
                                                fontSize: "13px"
                                            }}
                                        >
                                            • {item}
                                        </div>
                                    )
                                )}
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    )
}
