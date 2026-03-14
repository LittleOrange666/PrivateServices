import {Modal} from 'bootstrap';

/**
 * Shows a Bootstrap modal and returns a promise that resolves when the modal is hidden.
 * @param {string} title - The title of the modal.
 * @param {string} text - The body text of the modal.
 * @param {number|null} timeout - Auto-hide timeout in milliseconds.
 * @returns {Promise<void>}
 */
export function show_modal(title: string, text: string, timeout?: number): Promise<void> {
    if (!timeout && title === "成功") {
        timeout = 3000;
    }
    return new Promise((resolve) => {
        const modalElement = document.getElementById('myModal');
        if (!modalElement) {
            console.error('Modal element #myModal not found in the DOM.');
            return resolve(); // Resolve immediately if modal doesn't exist
        }

        const myModal = Modal.getOrCreateInstance(modalElement);

        const modalTitleEl = modalElement.querySelector('.modal-title');
        const modalBodyEl = modalElement.querySelector('.modal-body');

        if (modalTitleEl) modalTitleEl.textContent = title;
        if (modalBodyEl) modalBodyEl.textContent = text;

        let hideHandler = () => resolve();

        if (timeout) {
            const close_evt = () => myModal.hide();
            const timeout_id = window.setTimeout(close_evt, timeout);

            const keypressHandler = (event: KeyboardEvent) => {
                if (event.key) {
                    close_evt();
                }
            };
            document.addEventListener("keypress", keypressHandler, {once: true});

            // Overwrite hideHandler to also clean up listeners
            const originalHideHandler = hideHandler;
            hideHandler = () => {
                window.clearTimeout(timeout_id);
                document.removeEventListener("keypress", keypressHandler);
                originalHideHandler();
            };
        }

        modalElement.addEventListener("hide.bs.modal", hideHandler, {once: true});
        myModal.show();
    });
}

/**
 * Displays a confirmation modal and returns a promise that resolves with the user's choice.
 * This function requires a modal with the ID 'checkingModal' and a confirm button with the ID 'checkingModalEnter' to be present in the DOM.
 * @param {string} title - The title of the confirmation modal.
 * @param {string} [subtitle] - The body text of the modal. If not provided, a default message will be used.
 * @returns {Promise<boolean>} A promise that resolves to `true` if the user confirms, and `false` if the user cancels or dismisses the modal.
 */
export function double_check(title: string, subtitle?: string): Promise<boolean> {
    return new Promise((resolve) => {
        const modalElement = document.getElementById('checkingModal');
        if (!modalElement) {
            console.error('Modal element #checkingModal not found in the DOM.');
            return resolve(false); // Resolve with false if modal doesn't exist
        }

        const checkModal = Modal.getOrCreateInstance(modalElement);
        const modalTitleEl = modalElement.querySelector('.modal-title');
        const modalBodyEl = modalElement.querySelector('.modal-body');
        const enterButton = document.getElementById('checkingModalEnter');

        if (!enterButton) {
            console.error('Enter button #checkingModalEnter not found in the DOM.');
            return resolve(false);
        }

        if (modalTitleEl) modalTitleEl.textContent = title;
        if (modalBodyEl) modalBodyEl.textContent = subtitle || "請確認是否要繼續進行此操作。";

        let closed = false;

        const cleanUp = () => {
            enterButton.removeEventListener("click", enterClickHandler);
            modalElement.removeEventListener('hidden.bs.modal', cancelClickHandler);
        };

        const enterClickHandler = () => {
            if (closed) return;
            closed = true;
            cleanUp();
            resolve(true);
            checkModal.hide();
        };

        const cancelClickHandler = () => {
            if (closed) return;
            closed = true;
            cleanUp();
            resolve(false);
        };

        enterButton.addEventListener("click", enterClickHandler, {once: true});
        modalElement.addEventListener('hidden.bs.modal', cancelClickHandler, {once: true});

        checkModal.show();
    });
}
