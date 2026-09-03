(function () {
    const storageKey = "notes-site-sidebar-state";

    function loadState() {
        try {
            return JSON.parse(localStorage.getItem(storageKey)) || {};
        } catch (error) {
            return {};
        }
    }

    function saveState(state) {
        try {
            localStorage.setItem(storageKey, JSON.stringify(state));
        } catch (error) {
            // Continue to work when browser storage is unavailable.
        }
    }

    function setupSidebarToggles() {
        const header = document.querySelector(".md-header__inner");
        if (!header) return;

        const state = loadState();

        if (state.primary) {
            document.body.classList.add("sidebar-primary-collapsed");
        }
        if (state.secondary) {
            document.body.classList.add("sidebar-secondary-collapsed");
        }

        [
            {
                key: "primary",
                className: "sidebar-primary-collapsed",
                label: "收起左侧导航",
                collapsedLabel: "展开左侧导航",
                icon: "‹",
            },
            {
                key: "secondary",
                className: "sidebar-secondary-collapsed",
                label: "收起右侧大纲",
                collapsedLabel: "展开右侧大纲",
                icon: "›",
            },
        ].forEach(function (config) {
            const id = "sidebar-toggle-" + config.key;
            let button = document.getElementById(id);

            if (!button) {
                button = document.createElement("button");
                button.id = id;
                button.type = "button";
                button.className = "md-sidebar-toggle";
                button.innerHTML = '<span class="md-sidebar-toggle__icon" aria-hidden="true">' + config.icon + "</span>";
                header.appendChild(button);

                button.addEventListener("click", function () {
                    const collapsed = document.body.classList.toggle(config.className);
                    const nextState = loadState();
                    nextState[config.key] = collapsed;
                    saveState(nextState);
                    updateButton(button, config, collapsed);
                });
            }

            updateButton(button, config, document.body.classList.contains(config.className));
        });
    }

    function updateButton(button, config, collapsed) {
        button.setAttribute("aria-pressed", String(collapsed));
        button.setAttribute("aria-label", collapsed ? config.collapsedLabel : config.label);
        button.setAttribute("title", collapsed ? config.collapsedLabel : config.label);
    }

    if (typeof document$ !== "undefined") {
        document$.subscribe(setupSidebarToggles);
    } else {
        document.addEventListener("DOMContentLoaded", setupSidebarToggles);
    }
})();
