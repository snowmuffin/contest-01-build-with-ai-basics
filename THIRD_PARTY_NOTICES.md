# Dependency and asset record

Application code for the desktop aquarium is new in this repository. The solution and initial project files were bootstrapped with .NET SDK 10.0.202 templates, then adapted to the approved plan.

- .NET/WPF/Windows Forms: Microsoft .NET desktop framework; https://github.com/dotnet/wpf and https://github.com/dotnet/winforms (MIT). Runtime binaries are not redistributed by this G0 source step.
- MSTest 4.0.2: development-only dependency from the installed SDK template; resolved versions are recorded in the test project's `packages.lock.json`. https://github.com/microsoft/testfx (MIT).
- The notification icon currently uses the OS-provided `SystemIcons.Application` as a temporary G0 icon, not original artwork or a final product identity.
- G0 markers and feeder visuals are original simple drawing primitives, explicitly labelled temporary probes. No third-party fish/desktop-pet assets are incorporated.
- The Devpost Learn Skill Pack is development curriculum installed separately, not an implemented aquarium feature.

A project publication license and final asset provenance must be reviewed before public distribution. No license has been selected on the participant's behalf.
