# frontend/components/status_update.py

import streamlit as st

def show_status_update(
    message,
    status_type="info",
    show_header=True,
    header_text="Status Update"
):
    """
    Display a status update or next step to the candidate.

    Args:
        message (str): The status message to display.
        status_type (str): One of "info", "success", "warning", "error".
        show_header (bool): Whether to show a header above the message.
        header_text (str): Custom header text (default: "Status Update").
    """
    if show_header:
        st.subheader(f"🔔 {header_text}")

    if status_type == "info":
        st.info(message)
    elif status_type == "success":
        st.success(message)
    elif status_type == "warning":
        st.warning(message)
    elif status_type == "error":
        st.error(message)
    else:
        st.write(message)

# Example usage (for testing/demo)
if __name__ == "__main__":
    st.set_page_config(page_title="Status Update Demo")
    st.title("Status Update Demo")

    show_status_update(
        message="You have completed the technical section. Next up: Behavioral questions.",
        status_type="info"
    )

    show_status_update(
        message="Congratulations! You have completed the interview. You will receive an email update soon.",
        status_type="success"
    )

    show_status_update(
        message="Please answer all questions before proceeding.",
        status_type="warning"
    )

    show_status_update(
        message="There was a problem submitting your answer. Please try again.",
        status_type="error"
    )
