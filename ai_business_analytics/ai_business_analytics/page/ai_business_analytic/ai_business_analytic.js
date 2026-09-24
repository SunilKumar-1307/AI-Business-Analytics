frappe.pages["ai-business-analytic"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "AI Business Analytics",
        single_column: true
    });

    const html = `
        <div style="max-width: 1000px; margin: 30px auto; padding: 20px;">

            <h2>AI Business Analytics</h2>

            <p class="text-muted">
                Ask a natural-language question about your business data.
            </p>

            <div class="form-group" style="margin-top: 25px;">
                <label><strong>Business Question</strong></label>

                <textarea
                    id="ai-question"
                    class="form-control"
                    rows="3"
                    placeholder="Example: Show me sales by city for 2025"
                ></textarea>
            </div>

            <button
                id="ai-ask-button"
                class="btn btn-primary"
                style="margin-top: 10px;"
            >
                Ask Question
            </button>

            <div
                id="ai-loading"
                class="text-muted"
                style="display:none; margin-top:20px;"
            >
                Processing your question...
            </div>

            <div
                id="ai-result"
                style="display:none; margin-top:30px;"
            ></div>

        </div>
    `;

    $(page.main).html(html);

    $("#ai-ask-button").on("click", function () {
        const question = $("#ai-question").val().trim();

        if (!question) {
            frappe.msgprint("Please enter a business question.");
            return;
        }

        $("#ai-loading").show();
        $("#ai-result").hide();
        $("#ai-ask-button").prop("disabled", true);

        frappe.call({
            method: "ai_business_analytics.api.analytics.ask_question",
            args: {
                question: question
            },

            callback: function (response) {
                $("#ai-loading").hide();
                $("#ai-ask-button").prop("disabled", false);

                const result = response.message;

                if (!result) {
                    frappe.msgprint("No response received.");
                    return;
                }

                if (result.status === "unsupported") {
                    show_message(
                        result.message || "This question is not supported.",
                        "warning"
                    );
                    return;
                }

                if (result.status === "error") {
                    show_message(
                        result.message || "Unable to process the question.",
                        "danger"
                    );
                    return;
                }

                if (result.status === "success") {
                    render_result(result);
                }
            },

            error: function () {
                $("#ai-loading").hide();
                $("#ai-ask-button").prop("disabled", false);

                show_message(
                    "Unable to connect to the analytics service.",
                    "danger"
                );
            }
        });
    });

    function show_message(message, type) {
        $("#ai-result")
            .html(`
                <div class="alert alert-${type}">
                    ${frappe.utils.escape_html(message)}
                </div>
            `)
            .show();
    }

    function render_result(result) {
        let html = `
            <div class="card" style="color: #222;">
                <div class="card-body">

                    <h4>Result</h4>

                    <p>
                        <strong>Question:</strong>
                        ${frappe.utils.escape_html(result.question || "")}
                    </p>

                    <p>
                        <strong>Query type:</strong>
                        ${frappe.utils.escape_html(result.query_type || "")}
                    </p>
        `;

        if (Array.isArray(result.data) && result.data.length > 0) {
            const columns = Object.keys(result.data[0]);

            html += `
                <div class="table-responsive">
                    <table class="table table-bordered table-hover" style="color: #222;">
                        <thead>
                            <tr>
            `;

            columns.forEach(function (column) {
                html += `
                    <th>
                        ${frappe.utils.escape_html(column)}
                    </th>
                `;
            });

            html += `
                            </tr>
                        </thead>
                        <tbody>
            `;

            result.data.forEach(function (row) {
                html += "<tr>";

                columns.forEach(function (column) {
                    let value = row[column];

                    if (
                        typeof value === "number" &&
                        (
                            column.includes("amount") ||
                            column.includes("sales") ||
                            column.includes("revenue")
                        )
                    ) {
                        value = value.toLocaleString("en-IN", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2
                        });
                    }

                    html += `
                        <td>
                            ${frappe.utils.escape_html(
                                String(value ?? "")
                            )}
                        </td>
                    `;
                });

                html += "</tr>";
            });

            html += `
                        </tbody>
                    </table>
                </div>
            `;
        } else {
            html += `
                <div class="alert alert-info">
                    No data was returned.
                </div>
            `;
        }

        html += `
    <p style="margin-top:20px; color:#222 !important; font-weight:600;">
        Response time:
        <span style="color:#0b6e4f !important;">
            ${result.response_time_ms} ms
        </span>
    </p>
`;

        $("#ai-result").html(html).show();
    }
};
