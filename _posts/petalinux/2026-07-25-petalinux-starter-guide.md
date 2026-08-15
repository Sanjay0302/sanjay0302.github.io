---
layout: post
title: Petalinux Stater Guide
date: 2026-07-25 17:26 +0530
description: This blog will help you start with building customized linux for Xilinx based MPSOC (ZCU102) 
# image: https://www.centennialsoftwaresolutions.com/help/figure-out-petalinux-yocto-version/yocto_project_logo_1.png
image: 
  path: banner.gif
  # lqip helps in getting smother animation for large image size that loads slowly 
  lqip: data:image/webp;base64,UklGRpoAAABXRUJQVlA4WAoAAAAQAAAADwAABwAAQUxQSDIAAAARL0AmbZurmr57yyIiqE8oiG0bejIYEQTgqiDA9vqnsUSI6H+oAERp2HZ65qP/VIAWAFZQOCBCAAAA8AEAnQEqEAAIAAVAfCWkAALp8sF8rgRgAP7o9FDvMCkMde9PK7euH5M1m6VWoDXf2FkP3BqV0ZYbO6NA/VFIAAAA
  # alt: banner
category: [Embedded Linux, Xilinx]
tags: [petalinux, yocto, zcu102, mpsoc, fpga, bootloader]
author: sanjay0302
pin: false
math: true
mermaid: true
published: true
toc: true
comments: true
media_subpath: /_user_assets/petalinux/
---

<!-- Link Definitions -->
[petalinux-v2022.2-10141622-installer.run]: https://account.amd.com/en/forms/downloads/xef.html?filename=petalinux-v2022.2-10141622-installer.run
[xilinx-zcu102-v2022.2-10141622.bsp]: https://account.amd.com/en/forms/downloads/xef.html?filename=xilinx-zcu102-v2022.2-10141622.bsp
[downloads_2022.2_10071807.tar.gz]: https://account.amd.com/en/forms/downloads/xef.html?filename=downloads_2022.2_10071807.tar.gz
[sstate_aarch64_2022.2_10071807.tar.gz]: https://account.amd.com/en/forms/downloads/xef.html?filename=sstate_aarch64_2022.2_10071807.tar.gz
[sstate_arm_2022.2_10071807.tar.gz]: https://account.amd.com/en/forms/downloads/xef.html?filename=sstate_arm_2022.2_10071807.tar.gz
[microblaze_2022.2_10071807.tar.gz]: https://account.amd.com/en/forms/downloads/xef.html?filename=sstate_microblaze_2022.2_10071807.tar.gz
[Windows Web Installer]: https://account.amd.com/en/forms/downloads/xef.html?filename=Xilinx_Unified_2022.2_1014_8888_Win64.exe
[Linux Web Installer]: https://account.amd.com/en/forms/downloads/xef.html?filename=Xilinx_Unified_2022.2_1014_8888_Lin64.bin
[Unified Installer]: https://account.amd.com/en/forms/downloads/xef.html?filename=Xilinx_Unified_2022.2_1014_8888.tar.gz
[ubuntu-22.04.5-desktop-amd64.iso]: https://releases.ubuntu.com/jammy/
[Installation Requirements]: https://docs.amd.com/r/2022.2-English/ug1144-petalinux-tools-reference-guide/Installation-Requirements

# ZCU102 Petalinux Build

In this blog we will discuss how to build a BSP project for zcu102-mpsoc with graphical display manager and will look upon how to boot the kernel image from USB flash drive.

For a particular version of petalinux toolchain, try to use its recommended linux distro; The below list is for petalinux-2022.2.

1. [Ubuntu Jammy 22 Release][ubuntu-22.04.5-desktop-amd64.iso] is the supported OS for petalinux 2022.2
2. [petalinux-v2022.2-10141622-installer.run][petalinux-v2022.2-10141622-installer.run] contains the petalinux toochain.
3. [xilinx-zcu102-v2022.2-10141622.bsp][xilinx-zcu102-v2022.2-10141622.bsp] will be used to build a preconfigured mpsoc project, and we will be using this for our demonstration.
4. [downloads_2022.2_10071807.tar.gz][downloads_2022.2_10071807.tar.gz] contains all the necessary source files for building bsp project; download manually for offline builds.
5. [sstate_aarch64_2022.2_10071807.tar.gz][sstate_aarch64_2022.2_10071807.tar.gz] contains necessary cache files for arm64 to speed up the build process; download manually for offline builds.
6. [sstate_arm_2022.2_10071807.tar.gz][sstate_arm_2022.2_10071807.tar.gz] contains necessary cache files for arm32 to speed up the build process; download manually for offline builds.
7. [microblaze_2022.2_10071807.tar.gz][microblaze_2022.2_10071807.tar.gz] contains necessary cache files for microblaze to speed up the build process; download manually for offline builds.
8. Install Xilinx_Unified_2022.2_1014_8888 Vivado and Vitis.
   1. [Windows Web Installer][Windows Web Installer]
   2. [Linux Web Installer][Linux Web Installer]
   3. [Unified Installer][Unified Installer]
9. Follow the [Installation Requirements][Installation Requirements]

> Official download page for other versions of petalinux and vivado tools
>
> * [Vivado and Vitis](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/development-tools/2026-1.html)
> * [Petalinux Tools](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/embedded-software.html)
{: .prompt-info }

---

## Install Packages

```bash
# Pre-requisites
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install autoconf libtool texinfo gcc-multilib tmux screen \
    gdebi wget wine64 cmake make build-essential gawk \
    gcc g++ make binutils git gawk bison flex wget curl net-tools \
    iproute2 tftpd-hpa diffstat chrpath socat cpio unzip tar gzip \
    tofrodos libncurses5-dev libssl-dev xterm zlib1g-dev \
    openssh-server libxml-parser-perl libglib2.0-dev libgtk2.0-dev \
    minicom picocom gparted intltool gettext libtinfo5 libncurses5 -y

```

```bash
# After installing Vivado and Vitis manually install the cable drivers
cd <installed_location>/Vivado/2022.2/data/xicom/cable_drivers/lin64/install_script/install_drivers/
sudo ./install_drivers
```

## Install Petalinux Toolchain

```bash
mkdir -p ~/petalinux_downloads_sstate_shared/tools/petalinux/2022.2

tar -xvzf downloads_2022.2_10071807.tar.gz -C ~/petalinux_downloads_sstate_shared
tar -xvzf sstate_aarch64_2022.2_10071807.tar.gz -C ~/petalinux_downloads_sstate_shared
tar -xvzf sstate_arm_2022.2_10071807.tar.gz -C ~/petalinux_downloads_sstate_shared

./petalinux-v2022.2-10141622-installer.run -d ~/petalinux_downloads_sstate_shared/tools/petalinux/2022.2 --log petalinux_install.log
mkdir  -p ~/petalinux_project1
sudo chown -R $USER:$USER ~/petalinux_project1/

```

## Create project from BSP

```bash
cd ~/petalinux_project1/
source ~/petalinux_downloads_sstate_shared/tools/petalinux/2022.2/settings.sh
petalinux-create -t project -s ~/petalinux_downloads_sstate_shared/xilinx-zcu102-v2022.2-10141622.bsp -n zcu102_wayland
cd ./zcu102_wayland
```

---

## Petalinux Conifgs

```bash
# Configure the petalinux
petalinux-config
```

Search for below CONFIGS and set accordingly

* `CONFIG_YOCTO_LOCAL_SSTATE_FEEDS_URL` [`=/home/user/petalinux_downloads_sstate_shared/aarch64`]
* `CONFIG_PRE_MIRROR_URL` [=`file:///home/user/petalinux_downloads_sstate_shared/downloads`]
* `CONFIG_TMP_DIR_LOCATION` [=`${PROOT}/build/tmp`] keep this default
* `CONFIG_YOCTO_NETWORK_SSTATE_FEEDS` [=`n`]
* `CONFIG_YOCTO_BB_NO_NETWORK` [=`y`]

In this project will boot from NOR+USB so enable USB Boot EXT4 Format

* `CONFIG_SUBSYSTEM_ROOTFS_EXT4` [=`y`] ; select EXT4 from the menu; this helps us to boot from USB flash drive.
* `CONFIG_YOCTO_BB_NUMBER_THREADS` keep this default.
* `CONFIG_YOCTO_PARALLEL_MAKE` keep this default.

---

## Rootfs Configs

```bash
# Config the libraru and rootfs
petalinux-config -c rootfs
```

Here we are enabling wayland/weston display manager's package-group and related libraries.

* `CONFIG_libmali-xlnx` [=`y`];
* `CONFIG_mali-backend-wayland` [=`y`]
* `CONFIG_packagegroup-petalinux-weston` [=`y`]

> `petalinux` username is already added, upon first boot enter the `petalinux` username and the system will ask for new password; leave it empty if password not required
{: .prompt-info }

---

## Kernel Configs

```bash
# Configure Kernel
petalinux-config -c kernel
```

Need to enable these configs to properly use EFI and GPT Partition

* `CONFIG_PARTITION_ADVANCED` [=`y`]
* `CONFIG_EFI_PARTITION` [=`y`]
* `CONFIG_USB_DWC3` [=`y`]
* `CONFIG_USB_DWC3_DUAL_ROLE` [=`y`]
* `CONFIG_USB_SUPPORT` [=`y`]
* `CONFIG_USB_COMMON` [=`y`]
* `CONFIG_USB_ARCH_HAS_HCD` [=`y`]
* `CONFIG_USB` [=`y`]
* `CONFIG_USB_XHCI_HCD` [=`y`]
* `CONFIG_USB_XHCI_PLATFORM` [=`y`]

---

```bash
# Then builld the image
petalinux-build
```

---

> Jumper settings
>
> Refer [DWC3 Xilinx Linux USB driver](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841729/DWC3+Xilinx+Linux+USB+driver#Host-Mode)
>
> * Enable usb host mode (`J7 - ON` , `J113 - 1-2`, `J110 - 2-3`);
> * `J113` is beside the `J7`;
> * Connect `TX_ENABLE` jumper before trying to use SFP connector ; (`for ex, connect J16 for SFP0`)
{: .prompt-info }

---

> * The problem occurs specifically when connecting a USB 2.0 flash drive directly to the ZCU102's USB 3.0 Micro B upstream port—the protocol mismatch prevents proper enumeration in U-Boot and the kernel. Using a USB hub between them resolves this by allowing the hub's downstream port to negotiate USB 2.0 speeds.
> * Or try changing `maximum-speed` to `high-speed` to enable USB 2.0 instead of USB 3.0 `super-speed` in device tree; Refer [DWC3 Xilinx Linux USB driver](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841729/DWC3+Xilinx+Linux+USB+driver#Devicetree)
{: .prompt-danger }

---

## Preparing the Bootable Flash Drive

Use `gparted` tool and format the flash drive with ext4 format and create a single partition.

```bash
# Then copy the rootfs and boot
sudo mkdir -p /mnt/usb/boot

sudo mount /dev/sdb1 /mnt/usb

# Copy rootfs to /mnt/usb
sudo tar -xvf images/linux/rootfs.tar.gz -C /mnt/usb/

# Copy boot to /mnt/usb/boot
sudo cp images/linux/Image /mnt/usb/boot/
sudo cp images/linux/system.dtb /mnt/usb/boot/

sudo sync
sudo umount /mnt/usb
```

Then connect this flash drive with `Micro-B to USB-A` dongle along with an `usb hub`.

> We have enabled weston graphic manager and this leads to bigger rootfs size, since the jtag boot is not sufficient to properly boot this in on-shot, we will first run the initial bootloader in RAM and then using u-boot will boot the kernel image from flash drive.
{: .prompt-info }

---

## Booting Bootloaders

```bash
# flash the FSBL->TFA(BL31)->Uboot(BL33) directly to RAM
# BL31 Secure OS will also be included if enabled
petalinux-boot --jtag --u-boot
```

Load `pmufw.elf`, `zynqmp_fsbl.elf`, `bl31.elf`, `u-boot.elf` one after another from `${PROOT}/images/linux/` into RAM.

Open serial terminal alongside the bootloader flashing process, then upon interrupting the uboot auto booting, we will get uboot hush shell access.

```bash
# Use the minicom or picocom in seperate window parallely
# ttyUSB0 is default for Serial COM
sudo picocom -b 115200 /dev/ttyUSB0
```

| Boot Stage | Component Name              | Security State | Privilege Level |
| ---------- | --------------------------- | -------------- | --------------- |
| BL1        | BootROM                     | Secure         | EL3             |
| BL2        | Xilinx FSBL                 | Secure         | EL3             |
| BL31       | ARM Trusted Firmware (TF-A) | Secure         | EL3             |
| BL32       | OP-TEE / Secure OS          | Secure         | S-EL1           |
| BL33       | U-Boot                      | Non-Secure     | EL2             |
| OS         | Linux Kernel                | Non-Secure     | EL1             |

---

## Booting Kernel

```bash
ZynqMP> usb start # detects the HUB ports, onboard USB port and the connected flash drive
ZynqMP> ext4load usb 0:1 0x00200000 /boot/Image
ZynqMP> ext4load usb 0:1 0x00100000 /boot/system.dtb
ZynqMP> setenv bootargs "console=ttyPS0,115200 root=/dev/sda1 rw rootwait"
ZynqMP> booti 0x00200000 - 0x00100000
```

> The DP Port must be connected to display before booting or else manual weston service activation will be required.
{: .prompt-info }

---

## Enable Weston Session

> Since we are using kernel shell in `ttyPS*` psuedo terminal the graphical session and environment has to be manually configured.

```bash
$ mkdir -p /run/user/0
$ chmod 0700 /run/user/0
# sudo su
$ XDG_RUNTIME_DIR=/run/user/0 weston --backend=drm-backend.so --tty=1 --continue-without-input &
```

```bash
# Try to launch some GUI application
XDG_RUNTIME_DIR=/run/user/0 weston-terminal &
XDG_RUNTIME_DIR=/run/user/0 glmark2-es2-wayland &
```

```bash
# this throws random PRBS value on display using legacy frame buffer 
cat /dev/urandom > /dev/fb0
```
