import React from "react";
import Button from "src/components/Button/Button";
import { saveBotCapability } from "src/services/capabilityService";

const CapabilityForm = () => {
    const handleSave = async () => {
        const capabilityName = "Sample Capability"; // replace with actual input
        const capabilityDescription = "This is a description"; // replace with actual input
        const params = {}; // replace with actual params
        const configurationId = "123"; // replace with actual configuration ID

        await saveBotCapability(configurationId, capabilityName, capabilityDescription, params);
    };

    return (
        <div>
            {/* Other form elements */}
            <Button onClick={handleSave}>Save</Button>
            {/* Finish button has been removed */}
        </div>
    );
};
// REMOVED FINISH BUTTON AND NEW CHANGES MADE
